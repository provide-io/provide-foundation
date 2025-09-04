"""
Environment variable support for logger configuration.
Now delegates to the config system.
"""

from provide.foundation.logger.config import TelemetryConfig


def from_env() -> TelemetryConfig:
    """Creates a TelemetryConfig instance from environment variables."""
    return TelemetryConfig.from_env()