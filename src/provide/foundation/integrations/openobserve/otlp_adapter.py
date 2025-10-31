#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve-specific OTLP adapter extending generic client.

Provides OpenObserveOTLPClient that extends OTLPLogClient with OpenObserve-specific
configuration and customizations."""

from __future__ import annotations

import base64

from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.otlp.client import OTLPLogClient


def get_openobserve_otlp_endpoint(base_url: str, org: str | None = None, endpoint_type: str = "logs") -> str:
    """Derive OTLP endpoint from OpenObserve base URL.

    Handles:
    - URLs with /api/{org}/ path
    - URLs without /api/ path
    - Trailing slashes
    - Both logs and metrics endpoints

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")
        endpoint_type: Type of endpoint ("logs" or "metrics", defaults to "logs")

    Returns:
        OTLP endpoint URL

    Examples:
        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai/api/my-org/")
        'https://api.openobserve.ai/api/my-org/v1/logs'

        >>> get_openobserve_otlp_endpoint("https://api.openobserve.ai", "my-org", "metrics")
        'https://api.openobserve.ai/api/my-org/v1/metrics'
    """
    # Remove trailing slash
    url = base_url.rstrip("/")

    # Extract base URL if /api/ present
    if "/api/" in url:
        url = url.split("/api/")[0]

    # Build OTLP endpoint
    org_name = org or "default"
    return f"{url}/api/{org_name}/v1/{endpoint_type}"


def get_openobserve_otlp_metrics_endpoint(base_url: str, org: str | None = None) -> str:
    """Derive OTLP metrics endpoint from OpenObserve base URL.

    Convenience function that calls get_openobserve_otlp_endpoint with endpoint_type="metrics".

    Args:
        base_url: OpenObserve base URL
        org: Organization name (defaults to "default")

    Returns:
        OTLP metrics endpoint

    Examples:
        >>> get_openobserve_otlp_metrics_endpoint("https://api.openobserve.ai", "my-org")
        'https://api.openobserve.ai/api/my-org/v1/metrics'
    """
    return get_openobserve_otlp_endpoint(base_url, org, endpoint_type="metrics")


def build_openobserve_headers(
    oo_config: OpenObserveConfig,
    base_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build headers with OpenObserve-specific metadata.

    Adds:
    - organization header
    - stream-name header
    - Basic auth header (from user/password)

    Args:
        oo_config: OpenObserve configuration
        base_headers: Base headers to include

    Returns:
        Complete headers dict with OpenObserve metadata

    Examples:
        >>> config = OpenObserveConfig(
        ...     org="my-org",
        ...     stream="logs",
        ...     user="admin",
        ...     password="secret"
        ... )
        >>> headers = build_openobserve_headers(config)
        >>> "authorization" in headers
        True
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OpenObserve-specific headers
    if oo_config.org:
        headers["organization"] = oo_config.org

    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Add Basic auth
    if oo_config.user and oo_config.password:
        credentials = f"{oo_config.user}:{oo_config.password}"
        encoded = base64.b64encode(credentials.encode()).decode("ascii")
        headers["authorization"] = f"Basic {encoded}"

    return headers


class OpenObserveOTLPClient(OTLPLogClient):
    """OpenObserve-specific OTLP client with vendor customizations.

    Extends the generic OTLPLogClient with OpenObserve-specific configuration
    and header management.

    Examples:
        >>> from provide.foundation.integrations.openobserve.config import OpenObserveConfig
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> oo_config = OpenObserveConfig.from_env()
        >>> telemetry_config = TelemetryConfig.from_env()
        >>> client = OpenObserveOTLPClient.from_openobserve_config(
        ...     oo_config, telemetry_config
        ... )
        >>> client.send_log("Hello OpenObserve!")
        True
    """

    @classmethod
    def from_openobserve_config(
        cls,
        oo_config: OpenObserveConfig,
        telemetry_config: TelemetryConfig,
    ) -> OpenObserveOTLPClient:
        """Create OTLP client configured for OpenObserve.

        Derives OTLP settings from OpenObserve configuration:
        - Builds OTLP endpoint from OpenObserve URL
        - Adds OpenObserve headers (organization, stream)
        - Configures Basic auth from credentials

        Args:
            oo_config: OpenObserve configuration
            telemetry_config: Telemetry configuration

        Returns:
            Configured OpenObserveOTLPClient

        Raises:
            ValueError: If OpenObserve URL is not set

        Examples:
            >>> oo_config = OpenObserveConfig(
            ...     url="https://api.openobserve.ai",
            ...     org="my-org",
            ...     user="admin",
            ...     password="secret",
            ... )
            >>> telemetry_config = TelemetryConfig(service_name="my-service")
            >>> client = OpenObserveOTLPClient.from_openobserve_config(
            ...     oo_config, telemetry_config
            ... )
        """
        if not oo_config.url:
            msg = "OpenObserve URL must be set"
            raise ValueError(msg)

        # Build OTLP endpoint from OpenObserve URL
        endpoint = get_openobserve_otlp_endpoint(oo_config.url, oo_config.org)

        # Build headers with OpenObserve metadata
        headers = build_openobserve_headers(oo_config)

        # Merge with telemetry config headers
        if telemetry_config.otlp_headers:
            headers.update(telemetry_config.otlp_headers)

        return cls(
            endpoint=endpoint,
            headers=headers,
            service_name=telemetry_config.service_name or "foundation",
            service_version=telemetry_config.service_version,
        )

    @classmethod
    def from_env(cls) -> OpenObserveOTLPClient | None:
        """Create client from environment variables.

        Returns:
            Configured client if OpenObserve is configured, None otherwise

        Examples:
            >>> # With env vars set:
            >>> # OPENOBSERVE_URL=https://api.openobserve.ai
            >>> # OPENOBSERVE_ORG=my-org
            >>> # OPENOBSERVE_USER=admin
            >>> # OPENOBSERVE_PASSWORD=secret
            >>> client = OpenObserveOTLPClient.from_env()
            >>> if client:
            ...     client.send_log("Hello!")
        """
        try:
            oo_config = OpenObserveConfig.from_env()
            if not oo_config.is_configured():
                return None

            telemetry_config = TelemetryConfig.from_env()

            return cls.from_openobserve_config(oo_config, telemetry_config)
        except Exception:
            return None


__all__ = [
    "OpenObserveOTLPClient",
    "build_openobserve_headers",
    "get_openobserve_otlp_endpoint",
    "get_openobserve_otlp_metrics_endpoint",
]

# 🧱🏗️🔚
