#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File operation detection system with extensible registry.

This module provides a registry-based system for detecting file operation patterns
from file system events. Built-in detectors are automatically registered with
priorities, and custom detectors can be added via the registry API.

Architecture:
    - Protocol-based detector interface (DetectorFunc)
    - Priority-ordered execution (0-100, higher = earlier)
    - Extensible via register_detector()
    - Thread-safe singleton registry

Example - Using built-in detectors:
    >>> from provide.foundation.file.operations.detectors import OperationDetector
    >>> detector = OperationDetector()
    >>> operation = detector.detect_operation(events)

Example - Registering custom detector:
    >>> from provide.foundation.file.operations.detectors import register_detector
    >>> def detect_my_pattern(events):
    ...     # Custom detection logic
    ...     return FileOperation(...) if pattern_found else None
    >>> register_detector(
    ...     name="detect_custom",
    ...     func=detect_my_pattern,
    ...     priority=85,
    ...     description="Detects custom pattern"
    ... )"""

from __future__ import annotations

from provide.foundation.file.operations.detectors.atomic import (
    AtomicOperationDetector,
)
from provide.foundation.file.operations.detectors.batch import BatchOperationDetector
from provide.foundation.file.operations.detectors.orchestrator import OperationDetector
from provide.foundation.file.operations.detectors.protocol import DetectorFunc
from provide.foundation.file.operations.detectors.registry import (
    clear_detector_registry,
    get_all_detectors,
    get_detector_registry,
    register_detector,
)
from provide.foundation.file.operations.detectors.simple import SimpleOperationDetector
from provide.foundation.file.operations.detectors.temp import TempPatternDetector


def _auto_register_builtin_detectors() -> None:
    """Auto-register built-in detectors with their priorities.

    Priority scale (0-100, higher = earlier execution):
    - 90-100: Temp file patterns (highest specificity for atomic saves)
    - 80-89: Atomic save patterns
    - 70-79: Batch and sequence patterns
    - 60-69: Simple patterns (lower specificity)
    - 10-59: Reserved for custom detectors
    - 0-9: Fallback patterns (lowest priority)

    Registration is idempotent and thread-safe.
    """
    registry = get_detector_registry()

    # Check if already registered (idempotent)
    if registry.get("detect_temp_rename_pattern", dimension="file_operation_detector"):
        return

    # Create detector instances
    temp_detector = TempPatternDetector()
    atomic_detector = AtomicOperationDetector()
    batch_detector = BatchOperationDetector()
    simple_detector = SimpleOperationDetector()

    # Temp file patterns (highest specificity for atomic saves)
    register_detector(
        name="detect_temp_rename_pattern",
        func=temp_detector.detect_temp_rename_pattern,
        priority=95,
        description="Detects temp file rename pattern (create temp → rename to final)",
    )

    register_detector(
        name="detect_delete_temp_pattern",
        func=temp_detector.detect_delete_temp_pattern,
        priority=94,
        description="Detects delete temp pattern (delete original → create temp → rename temp)",
    )

    register_detector(
        name="detect_temp_modify_pattern",
        func=temp_detector.detect_temp_modify_pattern,
        priority=93,
        description="Detects temp modify pattern (create temp → modify temp → rename to final)",
    )

    register_detector(
        name="detect_temp_create_delete_pattern",
        func=temp_detector.detect_temp_create_delete_pattern,
        priority=92,
        description="Detects temp create/delete pattern (create temp → delete temp → create real file)",
    )

    # Atomic save patterns
    register_detector(
        name="detect_atomic_save",
        func=atomic_detector.detect_atomic_save,
        priority=85,
        description="Detects atomic save pattern (write to temp file, then rename)",
    )

    register_detector(
        name="detect_safe_write",
        func=atomic_detector.detect_safe_write,
        priority=84,
        description="Detects safe write pattern (backup original, write new, cleanup)",
    )

    # Batch and sequence patterns
    register_detector(
        name="detect_rename_sequence",
        func=batch_detector.detect_rename_sequence,
        priority=75,
        description="Detects rename sequence pattern (chain of moves: A → B → C)",
    )

    register_detector(
        name="detect_backup_create",
        func=batch_detector.detect_backup_create,
        priority=74,
        description="Detects backup creation pattern",
    )

    register_detector(
        name="detect_batch_update",
        func=batch_detector.detect_batch_update,
        priority=73,
        description="Detects batch update pattern (multiple related files updated together)",
    )

    # Simple patterns (lower specificity)
    register_detector(
        name="detect_same_file_delete_create_pattern",
        func=simple_detector.detect_same_file_delete_create_pattern,
        priority=65,
        description="Detects delete followed by create of same file (replace pattern)",
    )

    register_detector(
        name="detect_direct_modification",
        func=simple_detector.detect_direct_modification,
        priority=64,
        description="Detects direct file modification (multiple events on same file)",
    )

    # Fallback for unmatched events (lowest priority)
    register_detector(
        name="detect_simple_operation",
        func=simple_detector.detect_simple_operation,
        priority=10,
        description="Detects simple single-event operations (fallback)",
    )


# Auto-register built-in detectors on module import
_auto_register_builtin_detectors()


__all__ = [
    "AtomicOperationDetector",
    "BatchOperationDetector",
    "DetectorFunc",
    "OperationDetector",
    "SimpleOperationDetector",
    "TempPatternDetector",
    "clear_detector_registry",
    "get_all_detectors",
    "get_detector_registry",
    "register_detector",
]

# 🧱🏗️🔚
