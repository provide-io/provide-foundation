#
# telemetry.py
#
"""
TelemetryConfig class for Foundation telemetry configuration.
"""

from attrs import define

from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.base import field
from provide.foundation.config.defaults import (
    DEFAULT_TELEMETRY_GLOBALLY_DISABLED,
    DEFAULT_TRACING_ENABLED,
    DEFAULT_METRICS_ENABLED,
    DEFAULT_OTLP_PROTOCOL,
    DEFAULT_TRACE_SAMPLE_RATE,
)
import os
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_headers,
    parse_sample_rate,
    validate_sample_rate,
)
from provide.foundation.logger.config.logging import LoggingConfig


def _get_service_name() -> str | None:
    """Get service name from OTEL_SERVICE_NAME or PROVIDE_SERVICE_NAME (OTEL takes precedence)."""
    return os.getenv("OTEL_SERVICE_NAME") or os.getenv("PROVIDE_SERVICE_NAME")


@define(slots=True, repr=False)
class TelemetryConfig(RuntimeConfig):
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(
        factory=_get_service_name,
        description="Service name for telemetry (from OTEL_SERVICE_NAME or PROVIDE_SERVICE_NAME)",
    )
    service_version: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_VERSION",
        description="Service version for telemetry",
    )
    logging: LoggingConfig = field(
        factory=lambda: LoggingConfig.from_env(),
        description="Logging configuration"
    )
    globally_disabled: bool = field(
        default=DEFAULT_TELEMETRY_GLOBALLY_DISABLED,
        env_var="PROVIDE_TELEMETRY_DISABLED",
        converter=parse_bool_extended,
        description="Globally disable telemetry",
    )

    # OpenTelemetry configuration
    tracing_enabled: bool = field(
        default=DEFAULT_TRACING_ENABLED,
        env_var="OTEL_TRACING_ENABLED",
        converter=parse_bool_extended,
        description="Enable OpenTelemetry tracing",
    )
    metrics_enabled: bool = field(
        default=DEFAULT_METRICS_ENABLED,
        env_var="OTEL_METRICS_ENABLED",
        converter=parse_bool_extended,
        description="Enable OpenTelemetry metrics",
    )
    otlp_endpoint: str | None = field(
        default=None,
        env_var="OTEL_EXPORTER_OTLP_ENDPOINT",
        description="OTLP endpoint for traces and metrics",
    )
    otlp_traces_endpoint: str | None = field(
        default=None,
        env_var="OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
        description="OTLP endpoint specifically for traces",
    )
    otlp_headers: dict[str, str] = field(
        factory=lambda: {},
        env_var="OTEL_EXPORTER_OTLP_HEADERS",
        converter=parse_headers,
        description="Headers to send with OTLP requests (key1=value1,key2=value2)",
    )
    otlp_protocol: str = field(
        default=DEFAULT_OTLP_PROTOCOL,
        env_var="OTEL_EXPORTER_OTLP_PROTOCOL",
        description="OTLP protocol (grpc, http/protobuf)",
    )
    trace_sample_rate: float = field(
        default=DEFAULT_TRACE_SAMPLE_RATE,
        env_var="OTEL_TRACE_SAMPLE_RATE",
        converter=parse_sample_rate,
        validator=validate_sample_rate,
        description="Sampling rate for traces (0.0 to 1.0)",
    )



    def get_otlp_headers_dict(self) -> dict[str, str]:
        """Get OTLP headers dictionary.

        Returns:
            Dictionary of header key-value pairs
        """
        return self.otlp_headers
