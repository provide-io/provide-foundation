"""
Serialization utilities for Foundation.

Provides consistent serialization handling with validation,
testing support, and integration with Foundation's configuration system.
"""

from provide.foundation.serialization.core import (
    provide_dumps,
    provide_loads,
)

__all__ = [
    "provide_dumps",
    "provide_loads",
]
