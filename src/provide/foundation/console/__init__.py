"""
Console I/O utilities for standardized CLI input/output.

Provides pout(), perr(), and pin() functions for consistent I/O handling.
"""

from provide.foundation.console.input import (
    apin,
    apin_lines,
    apin_stream,
    pin,
    pin_lines,
    pin_stream,
)
from provide.foundation.console.output import perr, pout

__all__ = [
    # Output functions
    "perr",
    "pout",
    # Input functions
    "pin",
    "pin_lines",
    "pin_stream",
    # Async input functions
    "apin",
    "apin_lines",
    "apin_stream",
]
