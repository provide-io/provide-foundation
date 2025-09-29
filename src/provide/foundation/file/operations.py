"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).

All components are re-exported from the operations package for convenience.
"""

from __future__ import annotations

# Re-export all components for convenience
from provide.foundation.file.operations.detector import OperationDetector
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationType,
)
from provide.foundation.file.operations.utils import (
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)

__all__ = [
    "DetectorConfig",
    "FileEvent",
    # Types
    "FileEventMetadata",
    "FileOperation",
    # Detector
    "OperationDetector",
    "OperationType",
    # Utilities
    "detect_atomic_save",
    "extract_original_path",
    "group_related_events",
    "is_temp_file",
]
