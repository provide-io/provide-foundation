"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).

All components are re-exported from the operations package for convenience.
"""

from __future__ import annotations

# Main detector
from provide.foundation.file.operations.detectors import OperationDetector

# Types
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationType,
)

# Utilities
from provide.foundation.file.operations.utils import (
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)

__all__ = [
    # Types
    "DetectorConfig",
    "FileEvent",
    "FileEventMetadata",
    "FileOperation",
    # Main detector
    "OperationDetector",
    "OperationType",
    # Utilities
    "detect_atomic_save",
    "extract_original_path",
    "group_related_events",
    "is_temp_file",
]
