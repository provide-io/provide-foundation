#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""File operation detection and analysis.

This module provides intelligent detection and grouping of file system events
into logical operations (e.g., atomic saves, batch updates, rename sequences).

## Simple API (Recommended)

For most use cases, use the simple functional API:

    >>> from provide.foundation.file.operations import detect, Event, Operation
    >>>
    >>> events = [Event(...), Event(...)]
    >>> operation = detect(events)
    >>> if operation:
    ...     print(f"{operation.type}: {operation.path}")

## Advanced API

For streaming detection or custom configuration:

    >>> from provide.foundation.file.operations import create_detector, DetectorConfig
    >>>
    >>> config = DetectorConfig(time_window_ms=1000)
    >>> detector = create_detector(config)
    >>>
    >>> for event in event_stream:
    ...     if operation := detector.detect_streaming(event):
    ...         handle_operation(operation)"""

from __future__ import annotations

# ============================================================================
# SIMPLE API (Recommended for most users)
# ============================================================================
# Simple detection functions
from provide.foundation.file.operations.detect import (
    create_detector,
    detect,
    detect_all,
    detect_streaming,
)

# ============================================================================
# FULL API (For backward compatibility and advanced usage)
# ============================================================================
# Original detector class
from provide.foundation.file.operations.detectors import OperationDetector

# Simplified type aliases
# Complete type system
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileEvent as Event,
    FileEventMetadata,
    FileOperation,
    FileOperation as Operation,
    OperationType,
)

# Utility functions
from provide.foundation.file.operations.utils import (
    detect_atomic_save,
    extract_original_path,
    group_related_events,
    is_temp_file,
)

__all__ = [
    "DetectorConfig",
    "Event",
    "FileEvent",
    "FileEventMetadata",
    "FileOperation",
    "Operation",
    "OperationDetector",
    "OperationType",
    "create_detector",
    "detect",
    "detect_all",
    "detect_atomic_save",
    "detect_streaming",
    "extract_original_path",
    "group_related_events",
    "is_temp_file",
]

# 🧱🏗️🔚
