"""File operation detection and analysis package."""

from __future__ import annotations

# Import all components for backward compatibility
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
