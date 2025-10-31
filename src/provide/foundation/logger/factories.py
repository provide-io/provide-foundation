#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# factories.py
#
import threading
from typing import Any

"""Logger factory functions and simple setup utilities.

Circular Dependency Mitigation
-------------------------------
This module uses thread-local state to break circular dependencies between
the logger and hub systems. The _is_initializing flag prevents recursive
imports during Foundation initialization.

Design Pattern:
1. Check thread-local flag to detect initialization recursion
2. If already initializing, return basic structlog logger (fast path)
3. Otherwise, attempt to get configured logger from Hub
4. On any error (ImportError, RecursionError), fall back to basic structlog
5. Always clear the flag in finally block to prevent state poisoning

This pattern allows modules to safely import get_logger() without creating
circular dependencies, at the cost of some initialization complexity.
"""

_is_initializing = threading.local()
# Maximum recursion depth before forcing fallback (safety limit)
_MAX_RECURSION_DEPTH = 3


def get_logger(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


# 🧱🏗️🔚
