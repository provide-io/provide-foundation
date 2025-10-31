#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# Check for Click availability
try:
    import click  # noqa: F401

    _HAS_CLICK = True
except ImportError:
    _HAS_CLICK = False

from provide.foundation.console.input import (
    apin,
    apin_lines,
    apin_stream,
    pin,
    pin_lines,
    pin_stream,
)
from provide.foundation.console.output import perr, pout

"""Console I/O utilities for standardized CLI input/output.

Provides pout(), perr(), and pin() functions for consistent I/O handling.
"""

__all__ = [
    # Dependency flags
    "_HAS_CLICK",
    # Async input functions
    "apin",
    "apin_lines",
    "apin_stream",
    # Output functions
    "perr",
    # Input functions
    "pin",
    "pin_lines",
    "pin_stream",
    "pout",
]

# 🧱🏗️🔚
