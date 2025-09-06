"""
Foundation Telemetry Configuration Module.

Re-exports configuration classes from the new modular structure.
"""

from provide.foundation.logger.config.logging import LoggingConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig

__all__ = [
    "LoggingConfig", 
    "TelemetryConfig",
]