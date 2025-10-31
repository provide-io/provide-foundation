#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Registry for file operation detectors."""

from __future__ import annotations

from provide.foundation.file.operations.detectors.protocol import DetectorFunc
from provide.foundation.hub.registry import Registry

"""File operation detector registry.

Provides a centralized registry for file operation detector functions,
allowing both built-in and custom detectors to be registered with priorities.
"""

_detector_registry: Registry | None = None


def get_detector_registry() -> Registry:
    """Get the global detector registry singleton.

    Returns:
        Registry instance for file operation detectors
    """
    global _detector_registry
    if _detector_registry is None:
        _detector_registry = Registry()
    return _detector_registry


def register_detector(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def get_all_detectors() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def clear_detector_registry() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = get_detector_registry()
    registry.clear("file_operation_detector")


__all__ = [
    "clear_detector_registry",
    "get_all_detectors",
    "get_detector_registry",
    "register_detector",
]

# 🧱🏗️🔚
