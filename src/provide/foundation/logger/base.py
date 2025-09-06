#
# base.py
#
"""
Foundation Logger - Main Interface.

Re-exports the core logger components.
"""

from provide.foundation.logger.core import FoundationLogger, logger, _LAZY_SETUP_STATE
from provide.foundation.logger.factories import get_logger, setup_logging

__all__ = [
    "FoundationLogger",
    "logger",
    "get_logger", 
    "setup_logging",
]