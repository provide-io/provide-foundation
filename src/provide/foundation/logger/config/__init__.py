#
# __init__.py
#
"""
Foundation Logger Configuration Module.

Re-exports all configuration classes for convenient importing.
"""

from provide.foundation.logger.config.logging import LoggingConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig

__all__ = [
    "LoggingConfig",
    "TelemetryConfig",
]
