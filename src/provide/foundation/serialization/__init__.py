from __future__ import annotations

from provide.foundation.serialization.core import (
    provide_dumps,
    provide_loads,
)

"""Serialization utilities for Foundation.

Provides consistent serialization handling with validation,
testing support, and integration with Foundation's configuration system.
"""

__all__ = [
    "provide_dumps",
    "provide_loads",
]
