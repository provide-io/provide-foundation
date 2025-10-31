#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# ruff: noqa: RUF009
import os

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.converters import (
    parse_bool_extended,
    parse_headers,
    parse_sample_rate,
    validate_sample_rate,
)
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.logger.config.logging import LoggingConfig
from provide.foundation.logger.defaults import default_logging_config
from provide.foundation.telemetry.defaults import (
    DEFAULT_METRICS_ENABLED,
    DEFAULT_OTLP_PROTOCOL,
    DEFAULT_TELEMETRY_GLOBALLY_DISABLED,
    DEFAULT_TRACE_SAMPLE_RATE,
    DEFAULT_TRACING_ENABLED,
    default_otlp_headers,
)

"""TelemetryConfig class for Foundation telemetry configuration."""


def _get_service_name() -> str | None:
    """Get service name from OTEL_SERVICE_NAME or PROVIDE_SERVICE_NAME (OTEL takes precedence)."""
    return os.getenv("OTEL_SERVICE_NAME") or os.getenv("PROVIDE_SERVICE_NAME")


def _get_service_version() -> str | None:
    """Get service version from package metadata.

    Attempts to retrieve the version for the provide-foundation package.
    Returns None if version cannot be determined.

    Returns:
        Package version string or None
    """
    try:
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation")
    except Exception:
        # Suppress all errors and return None if version can't be determined
        return None


@define(slots=True, repr=False)
class TelemetryConfig(RuntimeConfig):
    """Main configuration object for the Foundation Telemetry system."""

    service_name: str | None = field(
        factory=_get_service_name,
        description="Service name for telemetry (from OTEL_SERVICE_NAME or PROVIDE_SERVICE_NAME)",
    )
    service_version: str | None = field(
        factory=_get_service_version,
        env_var="PROVIDE_SERVICE_VERSION",
        description="Service version for telemetry (auto-populated from package version)",
    )
    logging: LoggingConfig = field(
        factory=default_logging_config,
        description="Logging configuration",
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
        factory=default_otlp_headers,
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

    @classmethod
    def from_env(
        cls,
        prefix: str = "",
        delimiter: str = "_",
        case_sensitive: bool = False,
    ) -> TelemetryConfig:
        """Load configuration from environment variables.

        This method explicitly provides the from_env() interface
        to ensure it's available on TelemetryConfig directly.

        If OpenObserve is configured and reachable, OTLP settings are
        automatically configured if not already set.
        """
        # Load base configuration
        config = super().from_env(prefix=prefix, delimiter=delimiter, case_sensitive=case_sensitive)

        # Auto-configure OTLP if OpenObserve is available and OTLP not already configured
        if not config.otlp_endpoint:
            config = cls._auto_configure_openobserve_otlp(config)

        return config

    @classmethod
    def _auto_configure_openobserve_otlp(cls, config: TelemetryConfig) -> TelemetryConfig:
        """Auto-configure OTLP from OpenObserve if available.

        Args:
            config: Base TelemetryConfig

        Returns:
            Updated config with OTLP settings if OpenObserve is available

        """
        try:
            from provide.foundation.integrations.openobserve.config import OpenObserveConfig

            oo_config = OpenObserveConfig.from_env()

            # Only auto-configure if OpenObserve is configured
            if not oo_config.is_configured():
                return config

            # Get OTLP endpoint from OpenObserve
            otlp_endpoint = oo_config.get_otlp_endpoint()
            if not otlp_endpoint:
                return config

            # Build OTLP headers with OpenObserve metadata and auth
            otlp_headers = dict(config.otlp_headers)  # Copy existing headers
            if oo_config.org:
                otlp_headers["organization"] = oo_config.org
            if oo_config.stream:
                otlp_headers["stream-name"] = oo_config.stream

            # Add Basic auth if credentials are available
            if oo_config.user and oo_config.password:
                import base64

                credentials = f"{oo_config.user}:{oo_config.password}"
                encoded = base64.b64encode(credentials.encode()).decode("ascii")
                otlp_headers["authorization"] = f"Basic {encoded}"

            # Create updated config with OTLP settings
            # Use attrs.evolve to create a new instance with updated fields
            from attrs import evolve

            return evolve(
                config,
                otlp_endpoint=otlp_endpoint,
                otlp_headers=otlp_headers,
            )

        except ImportError:
            # OpenObserve integration not available
            return config
        except Exception:
            # Any error in auto-configuration should not break config loading
            return config

    def get_otlp_headers_dict(self) -> dict[str, str]:
        """Get OTLP headers dictionary.

        Returns:
            Dictionary of header key-value pairs

        """
        return self.otlp_headers


# 🧱🏗️🔚
