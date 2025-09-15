#
# base.py
#
"""Foundation Logger - Main Interface.

Re-exports the core logger components.
"""

from provide.foundation.logger.core import FoundationLogger, logger
from provide.foundation.logger.factories import get_logger

__all__ = [
    "FoundationLogger",
    "get_logger",
    "logger",
]
