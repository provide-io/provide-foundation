#
# base.py
#
"""
Foundation Logger - Main Interface.

Re-exports the core logger components.
"""

from provide.foundation.logger.core import FoundationLogger, logger
from provide.foundation.logger.factories import get_logger, setup_logging

# Alias for consistent naming convention
setup_logger = setup_logging

__all__ = [
    "FoundationLogger",
    "get_logger",
    "logger",
    "setup_logger",  # New consistent naming
    "setup_logging",  # Keep for backward compatibility
]
