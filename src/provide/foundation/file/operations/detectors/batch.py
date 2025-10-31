#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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


class BatchOperationDetector:
    """Detects batch operations and rename sequences."""

    def detect_rename_sequence(self, events: list[FileEvent]) -> FileOperation | None:
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

    def detect_batch_update(self, events: list[FileEvent]) -> FileOperation | None:
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

    def detect_backup_create(self, events: list[FileEvent]) -> FileOperation | None:
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

    def _files_are_related(self, events: list[FileEvent]) -> bool:
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

    def _longest_common_prefix(self, strings: list[str]) -> str:
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

    def _determine_batch_operation_type(self, events: list[FileEvent]) -> OperationType:
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


# 🧱🏗️🔚
