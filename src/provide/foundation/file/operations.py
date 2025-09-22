"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).

For backward compatibility, all components are re-exported from the operations package.
"""

from __future__ import annotations

# Re-export all components for backward compatibility
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
    # Types
    "FileEventMetadata",
    "FileEvent",
    "OperationType",
    "FileOperation",
    "DetectorConfig",
    # Detector
    "OperationDetector",
    # Utilities
    "detect_atomic_save",
    "is_temp_file",
    "extract_original_path",
    "group_related_events",
]
