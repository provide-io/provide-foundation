#
# core.py
#
"""
Foundation Telemetry Core Setup Functions.
"""

# Emoji resolver removed - using event sets now
from provide.foundation.setup import (
    reset_foundation_setup_for_testing,
    setup_telemetry,
    shutdown_foundation_telemetry,
)

__all__ = [
    "reset_foundation_setup_for_testing",
    "setup_telemetry",
    "shutdown_foundation_telemetry",
]
