"""
Production time utilities for Foundation.

Provides consistent time handling with Foundation integration,
better testability, and timezone awareness.
"""

from provide.foundation.time.core import (
    provide_now,
    provide_sleep,
    provide_time,
)

__all__ = [
    "provide_now",
    "provide_sleep",
    "provide_time",
]
