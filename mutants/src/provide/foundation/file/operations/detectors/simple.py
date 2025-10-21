# provide/foundation/file/operations/detectors/simple.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Simple operation detectors."""

from __future__ import annotations

from pathlib import Path

from provide.foundation.file.operations.detectors.helpers import is_backup_file
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


class SimpleOperationDetector:
    """Detects simple, direct file operations."""

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_orig(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_1(
        self, events: list[FileEvent], window_ms: int = 1001
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_2(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) <= 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_3(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 3:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_4(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = None
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_5(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = None
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_6(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(None)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_7(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_8(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = None
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_9(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(None)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_10(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) <= 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_11(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 3:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_12(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                break

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_13(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=None)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_14(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: None)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_15(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(None):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_16(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) + 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_17(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 2):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_18(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = None
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_19(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = None

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_20(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i - 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_21(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 2]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_22(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" or create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_23(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type != "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_24(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "XXdeletedXX" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_25(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "DELETED" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_26(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type != "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_27(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "XXcreatedXX":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_28(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "CREATED":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_29(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = None

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_30(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() / 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_31(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp + delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_32(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1001

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_33(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff < window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_34(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=None,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_35(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=None,
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_36(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=None,
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_37(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=None,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_38(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=None,
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_39(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=None,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_40(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=None,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_41(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=None,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_42(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=None,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_43(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=None,
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_44(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata=None,
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_45(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_46(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_47(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_48(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_49(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_50(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_51(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_52(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_53(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_54(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_55(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_56(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(None),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_57(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=1.9,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_58(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(None).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_59(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=False,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_60(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=False,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_61(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(None)],
                            metadata={
                                "pattern": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_62(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "XXpatternXX": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_63(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "PATTERN": "delete_create_replace",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_64(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "XXdelete_create_replaceXX",
                            },
                        )

        return None

    def xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_65(
        self, events: list[FileEvent], window_ms: int = 1000
    ) -> FileOperation | None:
        """Detect delete followed by create of same file (replace pattern)."""
        if len(events) < 2:
            return None

        # Group events by path
        path_groups: dict[str, list[FileEvent]] = {}
        for event in events:
            path_str = str(event.path)
            if path_str not in path_groups:
                path_groups[path_str] = []
            path_groups[path_str].append(event)

        for path_str, path_events in path_groups.items():
            if len(path_events) < 2:
                continue

            path_events.sort(key=lambda e: e.timestamp)

            # Look for delete followed by create
            for i in range(len(path_events) - 1):
                delete_event = path_events[i]
                create_event = path_events[i + 1]

                if delete_event.event_type == "deleted" and create_event.event_type == "created":
                    time_diff = (create_event.timestamp - delete_event.timestamp).total_seconds() * 1000

                    if time_diff <= window_ms:
                        return FileOperation(
                            operation_type=OperationType.ATOMIC_SAVE,
                            primary_path=Path(path_str),
                            events=[delete_event, create_event],
                            confidence=0.90,
                            description=f"File replaced: {Path(path_str).name}",
                            start_time=delete_event.timestamp,
                            end_time=create_event.timestamp,
                            is_atomic=True,
                            is_safe=True,
                            files_affected=[Path(path_str)],
                            metadata={
                                "pattern": "DELETE_CREATE_REPLACE",
                            },
                        )

        return None
    
    xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_1': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_1, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_2': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_2, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_3': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_3, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_4': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_4, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_5': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_5, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_6': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_6, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_7': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_7, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_8': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_8, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_9': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_9, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_10': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_10, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_11': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_11, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_12': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_12, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_13': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_13, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_14': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_14, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_15': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_15, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_16': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_16, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_17': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_17, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_18': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_18, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_19': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_19, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_20': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_20, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_21': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_21, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_22': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_22, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_23': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_23, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_24': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_24, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_25': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_25, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_26': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_26, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_27': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_27, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_28': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_28, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_29': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_29, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_30': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_30, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_31': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_31, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_32': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_32, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_33': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_33, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_34': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_34, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_35': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_35, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_36': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_36, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_37': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_37, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_38': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_38, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_39': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_39, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_40': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_40, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_41': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_41, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_42': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_42, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_43': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_43, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_44': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_44, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_45': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_45, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_46': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_46, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_47': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_47, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_48': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_48, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_49': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_49, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_50': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_50, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_51': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_51, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_52': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_52, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_53': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_53, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_54': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_54, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_55': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_55, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_56': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_56, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_57': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_57, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_58': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_58, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_59': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_59, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_60': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_60, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_61': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_61, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_62': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_62, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_63': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_63, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_64': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_64, 
        'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_65': xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_65
    }
    
    def detect_same_file_delete_create_pattern(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_orig"), object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_same_file_delete_create_pattern.__signature__ = _mutmut_signature(xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_orig)
    xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern__mutmut_orig.__name__ = 'xǁSimpleOperationDetectorǁdetect_same_file_delete_create_pattern'

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_orig(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_1(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) == 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_2(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 2:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_3(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = None

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_4(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[1]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_5(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = None

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_6(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "XXcreatedXX": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_7(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "CREATED": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_8(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "XXmodifiedXX": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_9(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "MODIFIED": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_10(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "XXdeletedXX": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_11(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "DELETED": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_12(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "XXmovedXX": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_13(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "MOVED": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_14(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_15(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = None

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_16(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type != "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_17(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "XXmovedXX":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_18(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "MOVED":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_19(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = None
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_20(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path and event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_21(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = None
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_22(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "XXoriginal_pathXX": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_23(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "ORIGINAL_PATH": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_24(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(None),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_25(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "XXpatternXX": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_26(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "PATTERN": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_27(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "XXsimple_moveXX",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_28(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "SIMPLE_MOVE",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_29(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = None
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_30(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = None

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_31(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "XXpatternXX": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_32(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "PATTERN": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_33(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = None

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_34(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(None)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_35(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=None,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_36(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=None,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_37(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=None,
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_38(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=None,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_39(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=None,
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_40(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=None,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_41(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=None,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_42(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=None,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_43(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=None,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_44(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=None,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_45(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=None,
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_46(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=None,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_47(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_48(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_49(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_50(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_51(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_52(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_53(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_54(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_55(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_56(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_57(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_58(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_59(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=1.7,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_60(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=False,
            is_safe=True,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )

    def xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_61(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect simple single-event operations."""
        if len(events) != 1:
            return None

        event = events[0]

        # Map event types to operation types
        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        if event.event_type not in type_mapping:
            return None

        operation_type = type_mapping[event.event_type]

        # Special handling for move operations
        if event.event_type == "moved":
            primary_path = event.dest_path or event.path
            metadata = {
                "original_path": str(event.path),
                "pattern": "simple_move",
            }
        else:
            primary_path = event.path
            metadata = {
                "pattern": f"simple_{event.event_type}",
            }

        # Check if this is a backup file
        is_backup_path = is_backup_file(primary_path)

        return FileOperation(
            operation_type=operation_type,
            primary_path=primary_path,
            events=[event],
            confidence=0.70,
            description=f"Simple {event.event_type} on {primary_path.name}",
            start_time=event.timestamp,
            end_time=event.timestamp,
            is_atomic=True,
            is_safe=False,
            has_backup=is_backup_path,
            files_affected=[primary_path],
            metadata=metadata,
        )
    
    xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_1': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_1, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_2': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_2, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_3': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_3, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_4': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_4, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_5': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_5, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_6': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_6, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_7': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_7, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_8': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_8, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_9': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_9, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_10': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_10, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_11': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_11, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_12': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_12, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_13': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_13, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_14': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_14, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_15': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_15, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_16': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_16, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_17': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_17, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_18': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_18, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_19': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_19, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_20': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_20, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_21': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_21, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_22': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_22, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_23': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_23, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_24': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_24, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_25': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_25, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_26': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_26, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_27': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_27, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_28': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_28, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_29': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_29, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_30': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_30, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_31': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_31, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_32': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_32, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_33': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_33, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_34': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_34, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_35': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_35, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_36': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_36, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_37': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_37, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_38': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_38, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_39': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_39, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_40': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_40, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_41': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_41, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_42': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_42, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_43': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_43, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_44': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_44, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_45': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_45, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_46': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_46, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_47': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_47, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_48': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_48, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_49': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_49, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_50': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_50, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_51': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_51, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_52': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_52, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_53': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_53, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_54': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_54, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_55': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_55, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_56': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_56, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_57': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_57, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_58': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_58, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_59': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_59, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_60': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_60, 
        'xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_61': xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_61
    }
    
    def detect_simple_operation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_orig"), object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_simple_operation.__signature__ = _mutmut_signature(xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_orig)
    xǁSimpleOperationDetectorǁdetect_simple_operation__mutmut_orig.__name__ = 'xǁSimpleOperationDetectorǁdetect_simple_operation'

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_orig(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_1(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) <= 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_2(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 3:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_3(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = None
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_4(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[1]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_5(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_6(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(None):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_7(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path != first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_8(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = None

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_9(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(None, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_10(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=None)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_11(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_12(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, )

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_13(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: None)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_14(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = None
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_15(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = None
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_16(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(None)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_17(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et != "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_18(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "XXmodifiedXX" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_19(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "MODIFIED" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_20(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = None

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_21(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" or all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_22(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[1] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_23(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] != "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_24(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "XXcreatedXX" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_25(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "CREATED" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_26(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            None
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_27(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et != "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_28(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "XXmodifiedXX" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_29(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "MODIFIED" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_30(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[2:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_31(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_32(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies and is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_33(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = None
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_34(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = None
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_35(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = None
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_36(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = None

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_37(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=None,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_38(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=None,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_39(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=None,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_40(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=None,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_41(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=None,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_42(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=None,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_43(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=None,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_44(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=None,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_45(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=None,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_46(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=None,
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_47(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata=None,
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_48(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_49(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_50(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_51(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_52(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_53(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_54(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_55(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_56(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_57(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_58(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_59(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=1.8,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_60(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[1].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_61(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[+1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_62(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-2].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_63(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=True,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_64(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=False,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_65(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "XXevent_countXX": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_66(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "EVENT_COUNT": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_67(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "XXpatternXX": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_68(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "PATTERN": "direct_modification" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_69(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "XXdirect_modificationXX" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_70(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "DIRECT_MODIFICATION" if is_all_modifies else "create_modify",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_71(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "XXcreate_modifyXX",
            },
        )

    def xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_72(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect direct file modification (multiple events on same file)."""
        if len(events) < 2:
            return None

        # Check if all events are for the same file
        first_event = events[0]
        if not all(event.path == first_event.path for event in events):
            return None

        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Check if this is all modifies OR created followed by modifies
        event_types = [e.event_type for e in sorted_events]
        is_all_modifies = all(et == "modified" for et in event_types)
        is_create_then_modifies = event_types[0] == "created" and all(
            et == "modified" for et in event_types[1:]
        )

        if not (is_all_modifies or is_create_then_modifies):
            return None

        # Determine operation type based on pattern
        if is_create_then_modifies:
            op_type = OperationType.BACKUP_CREATE
            description = f"File created and modified: {first_event.path.name}"
        else:
            op_type = OperationType.ATOMIC_SAVE
            description = f"Multiple modifications to {first_event.path.name}"

        return FileOperation(
            operation_type=op_type,
            primary_path=first_event.path,
            events=sorted_events,
            confidence=0.80,
            description=description,
            start_time=sorted_events[0].timestamp,
            end_time=sorted_events[-1].timestamp,
            is_atomic=False,
            is_safe=True,
            files_affected=[first_event.path],
            metadata={
                "event_count": len(sorted_events),
                "pattern": "direct_modification" if is_all_modifies else "CREATE_MODIFY",
            },
        )
    
    xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_1': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_1, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_2': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_2, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_3': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_3, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_4': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_4, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_5': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_5, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_6': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_6, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_7': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_7, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_8': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_8, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_9': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_9, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_10': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_10, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_11': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_11, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_12': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_12, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_13': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_13, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_14': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_14, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_15': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_15, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_16': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_16, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_17': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_17, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_18': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_18, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_19': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_19, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_20': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_20, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_21': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_21, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_22': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_22, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_23': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_23, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_24': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_24, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_25': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_25, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_26': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_26, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_27': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_27, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_28': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_28, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_29': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_29, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_30': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_30, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_31': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_31, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_32': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_32, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_33': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_33, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_34': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_34, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_35': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_35, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_36': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_36, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_37': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_37, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_38': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_38, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_39': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_39, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_40': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_40, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_41': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_41, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_42': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_42, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_43': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_43, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_44': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_44, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_45': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_45, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_46': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_46, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_47': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_47, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_48': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_48, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_49': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_49, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_50': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_50, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_51': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_51, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_52': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_52, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_53': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_53, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_54': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_54, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_55': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_55, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_56': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_56, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_57': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_57, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_58': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_58, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_59': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_59, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_60': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_60, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_61': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_61, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_62': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_62, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_63': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_63, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_64': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_64, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_65': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_65, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_66': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_66, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_67': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_67, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_68': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_68, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_69': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_69, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_70': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_70, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_71': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_71, 
        'xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_72': xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_72
    }
    
    def detect_direct_modification(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_orig"), object.__getattribute__(self, "xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_direct_modification.__signature__ = _mutmut_signature(xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_orig)
    xǁSimpleOperationDetectorǁdetect_direct_modification__mutmut_orig.__name__ = 'xǁSimpleOperationDetectorǁdetect_direct_modification'


# <3 🧱🤝📄🪄
