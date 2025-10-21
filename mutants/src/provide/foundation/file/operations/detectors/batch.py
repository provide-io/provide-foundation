# provide/foundation/file/operations/detectors/batch.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Batch operation detectors."""

from __future__ import annotations

from collections import defaultdict

from provide.foundation.file.operations.detectors.helpers import is_backup_file, is_temp_file
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


class BatchOperationDetector:
    """Detects batch operations and rename sequences."""

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_orig(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_1(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) <= 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_2(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 3:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_3(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = None
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_4(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type != "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_5(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "XXmovedXX"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_6(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "MOVED"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_7(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) <= 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_8(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 3:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_9(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = None
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_10(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = None

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_11(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = None
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_12(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event or other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_13(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move == move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_14(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path != current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_15(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(None, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_16(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, None)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_17(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_18(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, )
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_19(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(1, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_20(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = None

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_21(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = None
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_22(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event or other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_23(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move == move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_24(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path != current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_25(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(None)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_26(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = None

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_27(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) > 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_28(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 3:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_29(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(None)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_30(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = None
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_31(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(None, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_32(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=None)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_33(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_34(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, )
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_35(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=None)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_36(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: None)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_37(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = None
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_38(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path and longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_39(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[+1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_40(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-2].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_41(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[+1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_42(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-2].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_43(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=None,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_44(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=None,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_45(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=None,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_46(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=None,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_47(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=None,
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_48(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=None,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_49(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=None,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_50(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=None,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_51(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=None,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_52(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=None,
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_53(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata=None,
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_54(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_55(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_56(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_57(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_58(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_59(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_60(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_61(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_62(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_63(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_64(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_65(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=1.9,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_66(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[1].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_67(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[+1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_68(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-2].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_69(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=False,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_70(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=False,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_71(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "XXoriginal_pathXX": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_72(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "ORIGINAL_PATH": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_73(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(None),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_74(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[1].path),
                    "chain_length": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_75(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "XXchain_lengthXX": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_76(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "CHAIN_LENGTH": len(longest_chain),
                    "pattern": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_77(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "XXpatternXX": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_78(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "PATTERN": "rename_sequence",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_79(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "XXrename_sequenceXX",
                },
            )

        return None

    def xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_80(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect rename sequence pattern."""
        if len(events) < 2:
            return None

        # Look for chain of moves: A -> B -> C
        move_events = [e for e in events if e.event_type == "moved"]
        if len(move_events) < 2:
            return None

        # Build rename chains
        chains = []
        for move_event in move_events:
            # Find chains where this move's source path is another move's destination
            chain = [move_event]

            # Look backwards
            current_src = move_event.path
            for other_move in move_events:
                if other_move != move_event and other_move.dest_path == current_src:
                    chain.insert(0, other_move)
                    current_src = other_move.path

            # Look forwards
            current_dest = move_event.dest_path
            for other_move in move_events:
                if other_move != move_event and other_move.path == current_dest:
                    chain.append(other_move)
                    current_dest = other_move.dest_path

            if len(chain) >= 2:
                chains.append(chain)

        # Find the longest chain
        if chains:
            longest_chain = max(chains, key=len)
            longest_chain.sort(key=lambda e: e.timestamp)

            final_path = longest_chain[-1].dest_path or longest_chain[-1].path
            return FileOperation(
                operation_type=OperationType.RENAME_SEQUENCE,
                primary_path=final_path,
                events=longest_chain,
                confidence=0.90,
                description=f"Rename sequence of {len(longest_chain)} moves",
                start_time=longest_chain[0].timestamp,
                end_time=longest_chain[-1].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[final_path],
                metadata={
                    "original_path": str(longest_chain[0].path),
                    "chain_length": len(longest_chain),
                    "pattern": "RENAME_SEQUENCE",
                },
            )

        return None
    
    xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_1': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_1, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_2': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_2, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_3': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_3, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_4': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_4, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_5': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_5, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_6': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_6, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_7': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_7, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_8': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_8, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_9': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_9, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_10': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_10, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_11': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_11, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_12': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_12, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_13': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_13, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_14': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_14, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_15': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_15, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_16': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_16, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_17': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_17, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_18': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_18, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_19': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_19, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_20': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_20, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_21': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_21, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_22': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_22, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_23': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_23, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_24': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_24, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_25': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_25, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_26': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_26, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_27': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_27, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_28': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_28, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_29': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_29, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_30': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_30, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_31': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_31, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_32': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_32, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_33': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_33, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_34': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_34, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_35': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_35, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_36': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_36, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_37': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_37, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_38': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_38, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_39': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_39, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_40': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_40, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_41': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_41, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_42': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_42, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_43': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_43, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_44': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_44, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_45': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_45, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_46': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_46, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_47': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_47, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_48': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_48, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_49': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_49, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_50': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_50, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_51': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_51, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_52': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_52, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_53': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_53, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_54': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_54, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_55': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_55, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_56': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_56, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_57': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_57, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_58': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_58, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_59': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_59, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_60': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_60, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_61': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_61, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_62': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_62, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_63': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_63, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_64': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_64, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_65': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_65, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_66': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_66, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_67': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_67, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_68': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_68, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_69': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_69, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_70': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_70, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_71': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_71, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_72': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_72, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_73': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_73, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_74': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_74, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_75': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_75, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_76': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_76, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_77': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_77, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_78': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_78, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_79': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_79, 
        'xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_80': xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_80
    }
    
    def detect_rename_sequence(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_rename_sequence.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_orig)
    xǁBatchOperationDetectorǁdetect_rename_sequence__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁdetect_rename_sequence'

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_orig(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_1(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) <= 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_2(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 4:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_3(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = None
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_4(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(None)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_5(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type not in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_6(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"XXcreatedXX", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_7(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"CREATED", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_8(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "XXmodifiedXX", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_9(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "MODIFIED", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_10(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "XXdeletedXX"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_11(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "DELETED"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_12(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(None)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_13(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) <= 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_14(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 4:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_15(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                break

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_16(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=None)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_17(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: None)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_18(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = None
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_19(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp + dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_20(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[+1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_21(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-2].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_22(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[1].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_23(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 or self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_24(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span < 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_25(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 6.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_26(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(None):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_27(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=None,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_28(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=None,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_29(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=None,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_30(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=None,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_31(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=None,
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_32(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=None,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_33(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=None,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_34(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=None,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_35(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=None,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_36(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=None,
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_37(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata=None,
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_38(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_39(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_40(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_41(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_42(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_43(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_44(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_45(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_46(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_47(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_48(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_49(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=1.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_50(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[1].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_51(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[+1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_52(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-2].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_53(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_54(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=False,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_55(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "XXfile_countXX": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_56(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "FILE_COUNT": len(dir_events),
                        "pattern": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_57(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "XXpatternXX": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_58(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "PATTERN": "batch_update",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_59(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "XXbatch_updateXX",
                    },
                )

        return None

    def xǁBatchOperationDetectorǁdetect_batch_update__mutmut_60(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect batch update pattern (multiple related files updated together)."""
        if len(events) < 3:
            return None

        # Group events by directory and time proximity
        directory_groups = defaultdict(list)
        for event in events:
            if event.event_type in {"created", "modified", "deleted"}:
                directory_groups[event.path.parent].append(event)

        for directory, dir_events in directory_groups.items():
            if len(dir_events) < 3:
                continue

            dir_events.sort(key=lambda e: e.timestamp)

            # Check if events are clustered in time (within 5 seconds)
            time_span = (dir_events[-1].timestamp - dir_events[0].timestamp).total_seconds()
            if time_span <= 5.0 and self._files_are_related(dir_events):
                return FileOperation(
                    operation_type=OperationType.BATCH_UPDATE,
                    primary_path=directory,
                    events=dir_events,
                    confidence=0.85,
                    description=f"Batch operation on {len(dir_events)} files",
                    start_time=dir_events[0].timestamp,
                    end_time=dir_events[-1].timestamp,
                    is_atomic=False,
                    is_safe=True,
                    files_affected=[e.path for e in dir_events],
                    metadata={
                        "file_count": len(dir_events),
                        "pattern": "BATCH_UPDATE",
                    },
                )

        return None
    
    xǁBatchOperationDetectorǁdetect_batch_update__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_1': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_1, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_2': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_2, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_3': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_3, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_4': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_4, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_5': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_5, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_6': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_6, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_7': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_7, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_8': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_8, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_9': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_9, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_10': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_10, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_11': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_11, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_12': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_12, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_13': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_13, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_14': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_14, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_15': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_15, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_16': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_16, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_17': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_17, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_18': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_18, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_19': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_19, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_20': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_20, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_21': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_21, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_22': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_22, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_23': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_23, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_24': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_24, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_25': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_25, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_26': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_26, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_27': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_27, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_28': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_28, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_29': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_29, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_30': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_30, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_31': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_31, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_32': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_32, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_33': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_33, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_34': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_34, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_35': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_35, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_36': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_36, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_37': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_37, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_38': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_38, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_39': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_39, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_40': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_40, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_41': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_41, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_42': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_42, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_43': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_43, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_44': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_44, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_45': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_45, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_46': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_46, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_47': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_47, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_48': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_48, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_49': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_49, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_50': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_50, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_51': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_51, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_52': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_52, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_53': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_53, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_54': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_54, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_55': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_55, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_56': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_56, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_57': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_57, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_58': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_58, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_59': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_59, 
        'xǁBatchOperationDetectorǁdetect_batch_update__mutmut_60': xǁBatchOperationDetectorǁdetect_batch_update__mutmut_60
    }
    
    def detect_batch_update(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_batch_update__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_batch_update__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_batch_update.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁdetect_batch_update__mutmut_orig)
    xǁBatchOperationDetectorǁdetect_batch_update__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁdetect_batch_update'

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_orig(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_1(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) <= 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_2(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 3:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_3(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(None):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_4(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) + 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_5(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 2):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_6(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = None
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_7(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = None

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_8(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i - 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_9(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 2]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_10(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path or not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_11(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path) or move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_12(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created" or is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_13(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved" or create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_14(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type != "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_15(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "XXmovedXX"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_16(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "MOVED"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_17(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type != "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_18(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "XXcreatedXX"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_19(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "CREATED"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_20(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(None)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_21(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path and move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_22(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path != create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_23(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_24(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(None)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_25(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = None
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_26(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp + move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_27(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff < 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_28(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 3.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_29(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=None,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_30(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=None,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_31(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=None,
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_32(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=None,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_33(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=None,
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_34(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=None,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_35(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=None,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_36(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=None,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_37(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=None,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_38(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=None,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_39(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=None,
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_40(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata=None,
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_41(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_42(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_43(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_44(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_45(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_46(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_47(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_48(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_49(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_50(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_51(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_52(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_53(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=1.9,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_54(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=False,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_55(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=False,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_56(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=False,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_57(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "XXbackup_fileXX": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_58(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "BACKUP_FILE": str(move_event.dest_path or move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_59(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(None),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_60(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path and move_event.path),
                            "pattern": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_61(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "XXpatternXX": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_62(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "PATTERN": "backup_create",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_63(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "XXbackup_createXX",
                        },
                    )

        return None

    def xǁBatchOperationDetectorǁdetect_backup_create__mutmut_64(self, events: list[FileEvent]) -> FileOperation | None:
        """Detect backup creation pattern."""
        if len(events) < 2:
            return None

        # Look for move to backup name followed by create of original
        for i in range(len(events) - 1):
            move_event = events[i]
            create_event = events[i + 1]

            if (
                move_event.event_type == "moved"
                and create_event.event_type == "created"
                and is_backup_file(move_event.dest_path or move_event.path)
                and move_event.path == create_event.path
                and not is_temp_file(create_event.path)
            ):
                # Time window check (backup operations usually happen quickly)
                time_diff = (create_event.timestamp - move_event.timestamp).total_seconds()
                if time_diff <= 2.0:
                    return FileOperation(
                        operation_type=OperationType.BACKUP_CREATE,
                        primary_path=create_event.path,
                        events=[move_event, create_event],
                        confidence=0.90,
                        description=f"Backup created for {create_event.path.name}",
                        start_time=move_event.timestamp,
                        end_time=create_event.timestamp,
                        is_atomic=True,
                        is_safe=True,
                        has_backup=True,
                        files_affected=[create_event.path],
                        metadata={
                            "backup_file": str(move_event.dest_path or move_event.path),
                            "pattern": "BACKUP_CREATE",
                        },
                    )

        return None
    
    xǁBatchOperationDetectorǁdetect_backup_create__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_1': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_1, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_2': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_2, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_3': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_3, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_4': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_4, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_5': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_5, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_6': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_6, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_7': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_7, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_8': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_8, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_9': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_9, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_10': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_10, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_11': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_11, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_12': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_12, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_13': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_13, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_14': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_14, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_15': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_15, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_16': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_16, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_17': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_17, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_18': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_18, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_19': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_19, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_20': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_20, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_21': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_21, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_22': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_22, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_23': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_23, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_24': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_24, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_25': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_25, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_26': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_26, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_27': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_27, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_28': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_28, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_29': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_29, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_30': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_30, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_31': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_31, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_32': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_32, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_33': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_33, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_34': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_34, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_35': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_35, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_36': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_36, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_37': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_37, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_38': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_38, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_39': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_39, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_40': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_40, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_41': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_41, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_42': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_42, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_43': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_43, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_44': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_44, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_45': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_45, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_46': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_46, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_47': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_47, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_48': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_48, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_49': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_49, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_50': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_50, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_51': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_51, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_52': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_52, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_53': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_53, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_54': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_54, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_55': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_55, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_56': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_56, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_57': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_57, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_58': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_58, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_59': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_59, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_60': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_60, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_61': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_61, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_62': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_62, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_63': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_63, 
        'xǁBatchOperationDetectorǁdetect_backup_create__mutmut_64': xǁBatchOperationDetectorǁdetect_backup_create__mutmut_64
    }
    
    def detect_backup_create(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_backup_create__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁdetect_backup_create__mutmut_mutants"), args, kwargs, self)
        return result 
    
    detect_backup_create.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁdetect_backup_create__mutmut_orig)
    xǁBatchOperationDetectorǁdetect_backup_create__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁdetect_backup_create'

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_orig(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_1(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) <= 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_2(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 3:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_3(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return True

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_4(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = None

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_5(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = None
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_6(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.upper() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_7(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 or extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_8(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) != 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_9(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 2 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_10(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions == {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_11(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {"XXXX"}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_12(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return False

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_13(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = None
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_14(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.upper() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_15(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) > 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_16(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 3:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_17(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = None
            return common_prefix_len >= 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_18(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len > 3

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_19(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 4

        return False

    def xǁBatchOperationDetectorǁ_files_are_related__mutmut_20(self, events: list[FileEvent]) -> bool:
        """Check if events involve related files."""
        if len(events) < 2:
            return False

        paths = [event.path for event in events]

        # Check for common extensions
        extensions = {path.suffix.lower() for path in paths}
        if len(extensions) == 1 and extensions != {""}:
            return True

        # Check for common prefixes/suffixes in names
        names = [path.stem.lower() for path in paths]
        if len(names) >= 2:
            # Simple heuristic: check if names share common prefixes
            common_prefix_len = len(self._longest_common_prefix([names[0], names[1]]))
            return common_prefix_len >= 3

        return True
    
    xǁBatchOperationDetectorǁ_files_are_related__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁ_files_are_related__mutmut_1': xǁBatchOperationDetectorǁ_files_are_related__mutmut_1, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_2': xǁBatchOperationDetectorǁ_files_are_related__mutmut_2, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_3': xǁBatchOperationDetectorǁ_files_are_related__mutmut_3, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_4': xǁBatchOperationDetectorǁ_files_are_related__mutmut_4, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_5': xǁBatchOperationDetectorǁ_files_are_related__mutmut_5, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_6': xǁBatchOperationDetectorǁ_files_are_related__mutmut_6, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_7': xǁBatchOperationDetectorǁ_files_are_related__mutmut_7, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_8': xǁBatchOperationDetectorǁ_files_are_related__mutmut_8, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_9': xǁBatchOperationDetectorǁ_files_are_related__mutmut_9, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_10': xǁBatchOperationDetectorǁ_files_are_related__mutmut_10, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_11': xǁBatchOperationDetectorǁ_files_are_related__mutmut_11, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_12': xǁBatchOperationDetectorǁ_files_are_related__mutmut_12, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_13': xǁBatchOperationDetectorǁ_files_are_related__mutmut_13, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_14': xǁBatchOperationDetectorǁ_files_are_related__mutmut_14, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_15': xǁBatchOperationDetectorǁ_files_are_related__mutmut_15, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_16': xǁBatchOperationDetectorǁ_files_are_related__mutmut_16, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_17': xǁBatchOperationDetectorǁ_files_are_related__mutmut_17, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_18': xǁBatchOperationDetectorǁ_files_are_related__mutmut_18, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_19': xǁBatchOperationDetectorǁ_files_are_related__mutmut_19, 
        'xǁBatchOperationDetectorǁ_files_are_related__mutmut_20': xǁBatchOperationDetectorǁ_files_are_related__mutmut_20
    }
    
    def _files_are_related(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁ_files_are_related__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁ_files_are_related__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _files_are_related.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁ_files_are_related__mutmut_orig)
    xǁBatchOperationDetectorǁ_files_are_related__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁ_files_are_related'

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_orig(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_1(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_2(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return "XXXX"

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_3(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = None
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_4(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(None)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_5(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = None

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_6(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = "XXXX"

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_7(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(None):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_8(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = None
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_9(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[1][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_10(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(None):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_11(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] != char for s in strings):
                common_prefix += char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_12(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix = char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_13(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix -= char
            else:
                break

        return common_prefix

    def xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_14(self, strings: list[str]) -> str:
        """Find longest common prefix of strings."""
        if not strings:
            return ""

        min_len = min(len(s) for s in strings)
        common_prefix = ""

        for i in range(min_len):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                return

        return common_prefix
    
    xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_1': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_1, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_2': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_2, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_3': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_3, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_4': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_4, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_5': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_5, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_6': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_6, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_7': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_7, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_8': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_8, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_9': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_9, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_10': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_10, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_11': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_11, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_12': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_12, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_13': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_13, 
        'xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_14': xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_14
    }
    
    def _longest_common_prefix(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _longest_common_prefix.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_orig)
    xǁBatchOperationDetectorǁ_longest_common_prefix__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁ_longest_common_prefix'

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_orig(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_1(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = None
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_2(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(None)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_3(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] = 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_4(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] -= 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_5(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 2

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_6(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = None

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_7(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(None, key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_8(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=None)

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_9(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_10(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), )

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_11(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: None)

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_12(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = None

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_13(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "XXcreatedXX": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_14(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "CREATED": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_15(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "XXmodifiedXX": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_16(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "MODIFIED": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_17(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "XXdeletedXX": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_18(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "DELETED": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_19(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "XXmovedXX": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_20(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "MOVED": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_21(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(None, OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_22(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, None)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_23(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(OperationType.BATCH_UPDATE)

    def xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_24(self, events: list[FileEvent]) -> OperationType:
        """Determine the primary operation type for a batch."""
        type_counts: dict[str, int] = defaultdict(int)
        for event in events:
            type_counts[event.event_type] += 1

        # Return the most common operation type
        most_common_type = max(type_counts.keys(), key=lambda k: type_counts[k])

        type_mapping = {
            "created": OperationType.BACKUP_CREATE,
            "modified": OperationType.ATOMIC_SAVE,
            "deleted": OperationType.TEMP_CLEANUP,
            "moved": OperationType.RENAME_SEQUENCE,
        }

        return type_mapping.get(most_common_type, )
    
    xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_1': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_1, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_2': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_2, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_3': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_3, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_4': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_4, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_5': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_5, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_6': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_6, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_7': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_7, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_8': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_8, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_9': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_9, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_10': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_10, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_11': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_11, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_12': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_12, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_13': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_13, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_14': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_14, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_15': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_15, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_16': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_16, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_17': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_17, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_18': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_18, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_19': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_19, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_20': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_20, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_21': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_21, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_22': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_22, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_23': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_23, 
        'xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_24': xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_24
    }
    
    def _determine_batch_operation_type(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_orig"), object.__getattribute__(self, "xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _determine_batch_operation_type.__signature__ = _mutmut_signature(xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_orig)
    xǁBatchOperationDetectorǁ_determine_batch_operation_type__mutmut_orig.__name__ = 'xǁBatchOperationDetectorǁ_determine_batch_operation_type'


# <3 🧱🤝📄🪄
