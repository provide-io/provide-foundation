#
# __init__.py
#
"""
Foundation Logger Setup Module.

Handles structured logging configuration, processor setup, and emoji resolution.
Provides the core setup functionality for the Foundation logging system.
"""

from provide.foundation.logger.setup.coordinator import (
    get_vanilla_logger,
    internal_setup,
)

# Import testing utilities conditionally
try:
    from provide.foundation.logger.setup.testing import (
        reset_foundation_setup_for_testing as reset_for_testing,
    )

    _has_testing = True
except ImportError:
    _has_testing = False
    reset_for_testing = None

__all__ = [
    "get_vanilla_logger",
    "internal_setup",
]

if _has_testing:
    __all__.append("reset_for_testing")
