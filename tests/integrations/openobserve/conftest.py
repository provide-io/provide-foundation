"""Fixtures and configuration for OpenObserve integration tests.

This module provides fixtures for integration tests that connect to a real
OpenObserve instance. Integration tests are skipped by default and require
the --integration flag to run.

Environment Variables (loaded via Foundation config):
    OPENOBSERVE_URL: OpenObserve instance URL
    OPENOBSERVE_USER: Username for authentication
    OPENOBSERVE_PASSWORD: Password for authentication
    OPENOBSERVE_ORG: Organization name (default: "default")
    OPENOBSERVE_STREAM: Stream name (default: "default")
    OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint for log sending
    OTEL_SERVICE_NAME: Service name for telemetry

Example:
    export OPENOBSERVE_URL=http://localhost:5080/api/default
    export OPENOBSERVE_USER=tim@provide.io
    export OPENOBSERVE_PASSWORD=password
    export OPENOBSERVE_ORG=default
    export OPENOBSERVE_STREAM=default

    pytest tests/integrations/openobserve/ --integration -v
"""

from __future__ import annotations

import pytest
import requests

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.exceptions import OpenObserveConfigError
from provide.foundation.logger.config.telemetry import TelemetryConfig


@pytest.fixture(scope="session")
def openobserve_config() -> OpenObserveConfig:
    """Load OpenObserve configuration from environment variables.

    Uses Foundation's config system to load from env vars:
    - OPENOBSERVE_URL
    - OPENOBSERVE_USER
    - OPENOBSERVE_PASSWORD
    - OPENOBSERVE_ORG
    - OPENOBSERVE_STREAM

    Returns:
        OpenObserveConfig instance loaded from environment

    """
    return OpenObserveConfig.from_env()


@pytest.fixture(scope="session")
def telemetry_config() -> TelemetryConfig:
    """Load Telemetry configuration from environment variables.

    Uses Foundation's config system to load from env vars:
    - OTEL_EXPORTER_OTLP_ENDPOINT
    - OTEL_SERVICE_NAME
    - etc.

    Returns:
        TelemetryConfig instance loaded from environment

    """
    return TelemetryConfig.from_env()


@pytest.fixture(scope="session")
def openobserve_client(openobserve_config: OpenObserveConfig) -> OpenObserveClient | None:
    """Create OpenObserve client if configuration is available.

    Uses Foundation's OpenObserveClient.from_config() which reads from
    the config system.

    Args:
        openobserve_config: OpenObserve configuration from fixture

    Returns:
        OpenObserveClient instance if configured, None otherwise

    """
    # Check if OpenObserve is configured
    if not openobserve_config.url:
        pytest.skip("OpenObserve not configured. Set OPENOBSERVE_URL to run integration tests.")
        return None

    if not openobserve_config.user or not openobserve_config.password:
        pytest.skip("OpenObserve credentials not configured. Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD.")
        return None

    try:
        # Create client using Foundation's from_config() method
        client = OpenObserveClient.from_config()
        return client
    except OpenObserveConfigError as e:
        pytest.skip(f"OpenObserve configuration error: {e}")
        return None


@pytest.fixture(scope="session")
def openobserve_available(openobserve_client: OpenObserveClient | None) -> bool:
    """Check if OpenObserve instance is reachable.

    Args:
        openobserve_client: OpenObserve client from fixture

    Returns:
        True if OpenObserve is reachable, False otherwise

    """
    if not openobserve_client:
        return False

    try:
        # Try to connect to OpenObserve health endpoint or list streams
        response = requests.get(
            f"{openobserve_client.url}/healthz",
            timeout=5,
            headers=openobserve_client.session.headers,
        )
        return response.status_code == 200
    except Exception:
        # If health check fails, try listing streams as fallback
        try:
            openobserve_client.list_streams()
            return True
        except Exception:
            pytest.skip(f"OpenObserve instance at {openobserve_client.url} is not reachable")
            return False


@pytest.fixture
def skip_if_no_openobserve(openobserve_available: bool) -> None:
    """Skip test if OpenObserve is not available.

    This fixture can be used by tests that require a running OpenObserve
    instance.

    Args:
        openobserve_available: Availability flag from fixture

    """
    if not openobserve_available:
        pytest.skip("OpenObserve instance not available")


@pytest.fixture
def test_stream_name(openobserve_config: OpenObserveConfig) -> str:
    """Get the test stream name from configuration.

    Args:
        openobserve_config: OpenObserve configuration

    Returns:
        Stream name for tests (defaults to "default")

    """
    return openobserve_config.stream or "default"


@pytest.fixture
def test_organization(openobserve_config: OpenObserveConfig) -> str:
    """Get the test organization name from configuration.

    Args:
        openobserve_config: OpenObserve configuration

    Returns:
        Organization name for tests (defaults to "default")

    """
    return openobserve_config.org or "default"
