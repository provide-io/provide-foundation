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
    service_version: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_VERSION",
        description="Service version for telemetry",
    )
    logging: LoggingConfig = field(
        factory=LoggingConfig, description="Logging configuration"
    )
    globally_disabled: bool = field(
        default=False,
        env_var="PROVIDE_TELEMETRY_DISABLED",
        description="Globally disable telemetry",
    )

    # OpenTelemetry configuration
    tracing_enabled: bool = field(
        default=True,
        env_var="OTEL_TRACING_ENABLED",
        description="Enable OpenTelemetry tracing",
    )
    metrics_enabled: bool = field(
        default=True,
        env_var="OTEL_METRICS_ENABLED",
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
    otlp_headers: str | None = field(
        default=None,
        env_var="OTEL_EXPORTER_OTLP_HEADERS",
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

        # Service version
        service_version = os.getenv("OTEL_SERVICE_VERSION") or os.getenv(
            "PROVIDE_SERVICE_VERSION"
        )
        if service_version:
            config_dict["service_version"] = service_version

        # Telemetry disable flag
        if disabled := os.getenv("PROVIDE_TELEMETRY_DISABLED"):
            config_dict["globally_disabled"] = disabled.lower() == "true"

        # OpenTelemetry specific configuration
        if tracing_enabled := os.getenv("OTEL_TRACING_ENABLED"):
            config_dict["tracing_enabled"] = tracing_enabled.lower() == "true"

        if metrics_enabled := os.getenv("OTEL_METRICS_ENABLED"):
            config_dict["metrics_enabled"] = metrics_enabled.lower() == "true"

        if otlp_endpoint := os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
            config_dict["otlp_endpoint"] = otlp_endpoint

        if otlp_traces_endpoint := os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"):
            config_dict["otlp_traces_endpoint"] = otlp_traces_endpoint

        if otlp_headers := os.getenv("OTEL_EXPORTER_OTLP_HEADERS"):
            config_dict["otlp_headers"] = otlp_headers

        if otlp_protocol := os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL"):
            config_dict["otlp_protocol"] = otlp_protocol

        if trace_sample_rate := os.getenv("OTEL_TRACE_SAMPLE_RATE"):
            try:
                config_dict["trace_sample_rate"] = float(trace_sample_rate)
            except ValueError:
                if strict:
                    raise
                # Use default value in non-strict mode

        # OpenObserve configuration
        if openobserve_url := os.getenv("OPENOBSERVE_URL"):
            config_dict["openobserve_url"] = openobserve_url

        if openobserve_org := os.getenv("OPENOBSERVE_ORG"):
            config_dict["openobserve_org"] = openobserve_org

        if openobserve_user := os.getenv("OPENOBSERVE_USER"):
            config_dict["openobserve_user"] = openobserve_user

        if openobserve_password := os.getenv("OPENOBSERVE_PASSWORD"):
            config_dict["openobserve_password"] = openobserve_password

        if openobserve_stream := os.getenv("OPENOBSERVE_STREAM"):
            config_dict["openobserve_stream"] = openobserve_stream

        # Load logging config from env
        config_dict["logging"] = LoggingConfig.from_env(strict=strict)

        return cls(**config_dict)

    def get_otlp_headers_dict(self) -> dict[str, str]:
        """Parse OTLP headers string into dictionary.

        Returns:
            Dictionary of header key-value pairs
        """
        if not self.otlp_headers:
            return {}

        headers = {}
        for pair in self.otlp_headers.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                headers[key.strip()] = value.strip()
        return headers
