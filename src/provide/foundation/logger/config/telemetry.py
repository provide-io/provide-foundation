#
# telemetry.py
#
"""
TelemetryConfig class for Foundation telemetry configuration.
"""

import os

from attrs import define

from provide.foundation.config.env import RuntimeConfig
from provide.foundation.config.base import field
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_headers,
    parse_sample_rate,
    validate_sample_rate,
)
from provide.foundation.logger.config.logging import LoggingConfig


@define(slots=True, repr=False)
class TelemetryConfig(RuntimeConfig):
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_NAME",
        converter=parse_service_name_with_otel_fallback,
        description="Service name for telemetry (falls back to OTEL_SERVICE_NAME)",
    )
    service_version: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_VERSION",
        converter=parse_service_version_with_otel_fallback,
        description="Service version for telemetry (falls back to OTEL_SERVICE_VERSION)",
    )
    logging: LoggingConfig = field(
        factory=lambda: LoggingConfig.from_env(),
        description="Logging configuration"
    )
    globally_disabled: bool = field(
        default=False,
        env_var="PROVIDE_TELEMETRY_DISABLED",
        converter=parse_bool_extended,
        description="Globally disable telemetry",
    )

    # OpenTelemetry configuration
    tracing_enabled: bool = field(
        default=True,
        env_var="OTEL_TRACING_ENABLED",
        converter=parse_bool_extended,
        description="Enable OpenTelemetry tracing",
    )
    metrics_enabled: bool = field(
        default=True,
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
        default="http/protobuf",
        env_var="OTEL_EXPORTER_OTLP_PROTOCOL",
        description="OTLP protocol (grpc, http/protobuf)",
    )
    trace_sample_rate: float = field(
        default=1.0,
        env_var="OTEL_TRACE_SAMPLE_RATE",
        converter=parse_sample_rate,
        validator=validate_sample_rate,
        description="Sampling rate for traces (0.0 to 1.0)",
    )

    # OpenObserve configuration
    openobserve_url: str | None = field(
        default=None,
        env_var="OPENOBSERVE_URL",
        description="OpenObserve API endpoint URL",
    )
    openobserve_org: str = field(
        default="default",
        env_var="OPENOBSERVE_ORG",
        description="OpenObserve organization name",
    )
    openobserve_user: str | None = field(
        default=None,
        env_var="OPENOBSERVE_USER",
        description="OpenObserve username for authentication",
    )
    openobserve_password: str | None = field(
        default=None,
        env_var="OPENOBSERVE_PASSWORD",
        description="OpenObserve password for authentication",
    )
    openobserve_stream: str = field(
        default="default",
        env_var="OPENOBSERVE_STREAM",
        description="Default OpenObserve stream name",
    )


    def get_otlp_headers_dict(self) -> dict[str, str]:
        """Get OTLP headers dictionary.

        Returns:
            Dictionary of header key-value pairs
        """
        return self.otlp_headers
