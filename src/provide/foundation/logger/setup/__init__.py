#
# __init__.py
#
"""Foundation Logger Setup Module.

Handles structured logging configuration, processor setup, and emoji resolution.
Provides the core setup functionality for the Foundation logging system.
"""

from __future__ import annotations

from provide.foundation.logger.setup.coordinator import (
    get_vanilla_logger,
    internal_setup,
)

__all__ = [
    "get_vanilla_logger",
    "internal_setup",
]
