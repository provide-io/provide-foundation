#
# telemetry.py
#
"""
TelemetryConfig class for Foundation telemetry configuration.
"""

import os

from attrs import define

from provide.foundation.config import BaseConfig, field
from provide.foundation.logger.config.logging import LoggingConfig


@define(slots=True, repr=False)
class TelemetryConfig(BaseConfig):
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_NAME",
        description="Service name for telemetry",
    )
    logging: LoggingConfig = field(
        factory=LoggingConfig, description="Logging configuration"
    )
    globally_disabled: bool = field(
        default=False,
        env_var="PROVIDE_TELEMETRY_DISABLED",
        description="Globally disable telemetry",
    )

    @classmethod
    def from_env(cls, strict: bool = True) -> "TelemetryConfig":
        """Creates a TelemetryConfig instance from environment variables."""
        config_dict = {}

        # Check OTEL_SERVICE_NAME first, then PROVIDE_SERVICE_NAME
        service_name = os.getenv("OTEL_SERVICE_NAME") or os.getenv(
            "PROVIDE_SERVICE_NAME"
        )
        if service_name:
            config_dict["service_name"] = service_name

        if disabled := os.getenv("PROVIDE_TELEMETRY_DISABLED"):
            config_dict["globally_disabled"] = disabled.lower() == "true"

        # Load logging config from env
        config_dict["logging"] = LoggingConfig.from_env(strict=strict)

        return cls(**config_dict)