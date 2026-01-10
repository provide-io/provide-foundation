#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve client initialization and configuration.

This module tests client initialization, configuration loading, and basic setup.
Run with: pytest tests/integrations/openobserve/test_client_init_config.py -v"""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveAuthenticationError,
    OpenObserveConfigError,
)


class MockResponse:
    """Mock response object for testing."""

    def __init__(
        self,
        status: int = 200,
        body: bytes | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.body = body or b"{}"
        self._json_data = json_data or {}

    def is_success(self) -> bool:
        """Check if response is successful."""
        return 200 <= self.status < 300

    def json(self) -> dict[str, Any]:
        """Return JSON data."""
        return self._json_data


class TestClientInitialization(FoundationTestCase):
    """Tests for OpenObserveClient initialization."""

    def test_init_basic(self) -> None:
        """Test basic client initialization."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        assert client.url == "http://localhost:5080"
        assert client.username == "test@example.com"
        assert client.password == "password"
        assert client.organization == "default"
        assert client._client is not None

    def test_init_with_custom_org(self) -> None:
        """Test client initialization with custom organization."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
            organization="custom_org",
        )

        assert client.organization == "custom_org"

    def test_init_strips_trailing_slash(self) -> None:
        """Test that URL trailing slash is removed."""
        client = OpenObserveClient(
            url="http://localhost:5080/",
            username="test@example.com",
            password="password",
        )

        assert client.url == "http://localhost:5080"
        assert not client.url.endswith("/")

    def test_init_with_timeout(self) -> None:
        """Test client initialization with custom timeout."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
            timeout=60,
        )

        assert client._client.default_timeout == 60.0

    def test_init_validates_credentials(self) -> None:
        """Test that credentials are validated during initialization."""
        # Empty username should raise error
        with pytest.raises(OpenObserveAuthenticationError):
            OpenObserveClient(
                url="http://localhost:5080",
                username="",
                password="password",
            )

        # Empty password should raise error
        with pytest.raises(OpenObserveAuthenticationError):
            OpenObserveClient(
                url="http://localhost:5080",
                username="test@example.com",
                password="",
            )


class TestClientFromConfig(FoundationTestCase):
    """Tests for creating client from config."""

    def test_from_config_success(self) -> None:
        """Test creating client from config with valid settings."""
        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig"
        ) as mock_config_class:
            # Mock config
            mock_config = MagicMock()
            mock_config.url = "http://localhost:5080"
            mock_config.user = "test@example.com"
            mock_config.password = "password"
            mock_config.org = "test_org"
            mock_config_class.from_env.return_value = mock_config

            client = OpenObserveClient.from_config()

            assert client.url == "http://localhost:5080"
            assert client.username == "test@example.com"
            assert client.organization == "test_org"

    def test_from_config_default_org(self) -> None:
        """Test creating client from config with default organization."""
        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig"
        ) as mock_config_class:
            mock_config = MagicMock()
            mock_config.url = "http://localhost:5080"
            mock_config.user = "test@example.com"
            mock_config.password = "password"
            mock_config.org = None
            mock_config_class.from_env.return_value = mock_config

            client = OpenObserveClient.from_config()

            assert client.organization == "default"

    def test_from_config_missing_url(self) -> None:
        """Test creating client from config without URL."""
        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig"
        ) as mock_config_class:
            mock_config = MagicMock()
            mock_config.url = None
            mock_config.user = "test@example.com"
            mock_config.password = "password"
            mock_config_class.from_env.return_value = mock_config

            with pytest.raises(OpenObserveConfigError, match="URL not configured"):
                OpenObserveClient.from_config()

    def test_from_config_missing_credentials(self) -> None:
        """Test creating client from config without credentials."""
        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig"
        ) as mock_config_class:
            mock_config = MagicMock()
            mock_config.url = "http://localhost:5080"
            mock_config.user = None
            mock_config.password = None
            mock_config_class.from_env.return_value = mock_config

            with pytest.raises(OpenObserveConfigError, match="credentials not configured"):
                OpenObserveClient.from_config()

    def test_from_config_missing_password(self) -> None:
        """Test creating client from config with user but no password."""
        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig"
        ) as mock_config_class:
            mock_config = MagicMock()
            mock_config.url = "http://localhost:5080"
            mock_config.user = "test@example.com"
            mock_config.password = None
            mock_config_class.from_env.return_value = mock_config

            with pytest.raises(OpenObserveConfigError, match="credentials not configured"):
                OpenObserveClient.from_config()


__all__ = [
    "TestClientFromConfig",
    "TestClientInitialization",
]

# 🧱🏗️🔚
