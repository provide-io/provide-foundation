from __future__ import annotations

from typing import TYPE_CHECKING, Any

"""Centralized Click dependency handling.

This module contains all the logic for handling the optional 'click' package.
When click is not installed, stub implementations are provided that raise
helpful ImportErrors with installation instructions.
"""

if TYPE_CHECKING:
    pass

# Try to import click
try:
    import click

    _HAS_CLICK = True
except ImportError:
    _HAS_CLICK = False

# Provide stub when click is not available
if not _HAS_CLICK:
    from provide.foundation.utils.stubs import create_dependency_stub

    click: Any = create_dependency_stub("click", "cli")  # type: ignore[assignment,no-redef]


__all__ = ["_HAS_CLICK", "click"]
