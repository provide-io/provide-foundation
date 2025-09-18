from __future__ import annotations

#
# base.py
#
from provide.foundation.logger.core import FoundationLogger, logger
from provide.foundation.logger.factories import get_logger

"""Foundation Logger - Main Interface.

Re-exports the core logger components.
"""

__all__ = [
    "FoundationLogger",
    "get_logger",
    "logger",
]
