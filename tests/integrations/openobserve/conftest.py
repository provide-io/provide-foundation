#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

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

    pytest tests/integrations/openobserve/ --integration -v"""

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


@pytest.fixture
async def openobserve_client(openobserve_config: OpenObserveConfig) -> OpenObserveClient | None:
    """Create OpenObserve client if configuration is available.

    Uses Foundation's OpenObserveClient.from_config() which reads from
    the config system.

    Args:
        openobserve_config: OpenObserve configuration from fixture

    Yields:
        OpenObserveClient instance if configured

    Note:
        Changed from session to function scope to avoid event loop closure issues
        during cleanup. Each test gets its own client instance with proper cleanup.

    """
    # Check if OpenObserve is configured
    if not openobserve_config.url:
        pytest.skip("OpenObserve not configured. Set OPENOBSERVE_URL to run integration tests.")

    if not openobserve_config.user or not openobserve_config.password:
        pytest.skip("OpenObserve credentials not configured. Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD.")

    try:
        # Create client using Foundation's from_config() method
        client = OpenObserveClient.from_config()
    except OpenObserveConfigError as e:
        pytest.skip(f"OpenObserve configuration error: {e}")

    yield client

    # Cleanup: ensure transports are properly closed
    if hasattr(client, "_client") and client._client:
        await client._client.__aexit__(None, None, None)


@pytest.fixture(scope="session")
def openobserve_available(openobserve_config: OpenObserveConfig) -> bool:
    """Check if OpenObserve instance is reachable.

    Args:
        openobserve_config: OpenObserve configuration from fixture

    Returns:
        True if OpenObserve is reachable, False otherwise

    Note:
        Uses direct HTTP check instead of client to avoid async/event loop issues
        with session-scoped fixtures.

    """
    if not openobserve_config.url:
        return False

    if not openobserve_config.user or not openobserve_config.password:
        return False

    try:
        # Try to connect to OpenObserve by checking the streams endpoint
        # Use basic HTTP check with requests library since we're in a session-scoped fixture
        # The URL already includes /api/{org}, so we just append the endpoint
        auth = (openobserve_config.user, openobserve_config.password)

        # Try the streams endpoint as a connectivity test
        url = f"{openobserve_config.url.rstrip('/')}/streams"
        response = requests.get(
            url,
            timeout=5,
            auth=auth,
        )
        # Accept 200 (success) - 401 would mean bad credentials
        return response.status_code == 200
    except Exception as e:
        # If connection fails completely, assume unavailable
        pytest.skip(f"OpenObserve instance at {openobserve_config.url} is not reachable: {e}")
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


# 🧱🏗️🔚
