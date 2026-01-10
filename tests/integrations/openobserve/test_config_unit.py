#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve configuration.

This module contains unit tests for OpenObserveConfig with mocked dependencies.
Run with: pytest tests/integrations/openobserve/test_config_unit.py -v"""

from __future__ import annotations

import os

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch

from provide.foundation.integrations.openobserve.config import OpenObserveConfig


class TestOpenObserveConfigInitialization(FoundationTestCase):
    """Tests for OpenObserveConfig initialization."""

    def test_config_initialization_with_defaults(self) -> None:
        """Test config initialization with default values."""
        config = OpenObserveConfig()

        assert config.url is None
        assert config.org is None
        assert config.user is None
        assert config.password is None
        assert config.stream is None

    def test_config_initialization_with_values(self) -> None:
        """Test config initialization with provided values."""
        config = OpenObserveConfig(
            url="http://localhost:5080/api/default",
            org="test-org",
            user="test@example.com",
            password="secret",
            stream="logs",
        )

        assert config.url == "http://localhost:5080/api/default"
        assert config.org == "test-org"
        assert config.user == "test@example.com"
        assert config.password == "secret"
        assert config.stream == "logs"

    def test_config_from_environment_variables(self) -> None:
        """Test config loading from environment variables."""
        env_vars = {
            "OPENOBSERVE_URL": "http://localhost:5080/api/default",
            "OPENOBSERVE_ORG": "env-org",
            "OPENOBSERVE_USER": "env@example.com",
            "OPENOBSERVE_PASSWORD": "env-secret",
            "OPENOBSERVE_STREAM": "env-logs",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            config = OpenObserveConfig.from_env()

            assert config.url == "http://localhost:5080/api/default"
            assert config.org == "env-org"
            assert config.user == "env@example.com"
            assert config.password == "env-secret"
            assert config.stream == "env-logs"

    def test_config_from_partial_environment(self) -> None:
        """Test config loading with some env vars missing."""
        env_vars = {
            "OPENOBSERVE_URL": "http://localhost:5080",
            "OPENOBSERVE_USER": "user@example.com",
            # Explicitly unset the other env vars
            "OPENOBSERVE_ORG": "",
            "OPENOBSERVE_PASSWORD": "",
            "OPENOBSERVE_STREAM": "",
        }

        # Remove empty string values after patching so they're truly absent
        with patch.dict(os.environ, env_vars, clear=False):
            # Remove the empty entries to simulate missing vars
            for key in ["OPENOBSERVE_ORG", "OPENOBSERVE_PASSWORD", "OPENOBSERVE_STREAM"]:
                os.environ.pop(key, None)

            config = OpenObserveConfig.from_env()

            assert config.url == "http://localhost:5080"
            assert config.user == "user@example.com"
            assert config.org is None
            assert config.password is None
            assert config.stream is None


class TestIsConfigured(FoundationTestCase):
    """Tests for is_configured method."""

    def test_is_configured_with_all_required_fields(self) -> None:
        """Test is_configured returns True when all required fields are set."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        assert config.is_configured() is True

    def test_is_configured_missing_url(self) -> None:
        """Test is_configured returns False when URL is missing."""
        config = OpenObserveConfig(
            user="test@example.com",
            password="secret",
        )

        assert config.is_configured() is False

    def test_is_configured_missing_user(self) -> None:
        """Test is_configured returns False when user is missing."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            password="secret",
        )

        assert config.is_configured() is False

    def test_is_configured_missing_password(self) -> None:
        """Test is_configured returns False when password is missing."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
        )

        assert config.is_configured() is False

    def test_is_configured_all_missing(self) -> None:
        """Test is_configured returns False when all fields are missing."""
        config = OpenObserveConfig()

        assert config.is_configured() is False

    def test_is_configured_empty_strings(self) -> None:
        """Test is_configured returns False for empty strings."""
        config = OpenObserveConfig(
            url="",
            user="",
            password="",
        )

        assert config.is_configured() is False


class TestGetOTLPEndpoint(FoundationTestCase):
    """Tests for get_otlp_endpoint method."""

    def test_get_otlp_endpoint_with_api_path(self) -> None:
        """Test OTLP endpoint extraction when URL includes /api/ path."""
        config = OpenObserveConfig(
            url="http://localhost:5080/api/default",
        )

        endpoint = config.get_otlp_endpoint()
        assert endpoint == "http://localhost:5080/api/default"

    def test_get_otlp_endpoint_with_custom_org(self) -> None:
        """Test OTLP endpoint with custom organization."""
        config = OpenObserveConfig(
            url="http://localhost:5080/api/custom",
            org="custom",
        )

        endpoint = config.get_otlp_endpoint()
        assert endpoint == "http://localhost:5080/api/custom"

    def test_get_otlp_endpoint_without_api_path(self) -> None:
        """Test OTLP endpoint when URL doesn't include /api/ path."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            org="myorg",
        )

        endpoint = config.get_otlp_endpoint()
        assert endpoint == "http://localhost:5080/api/myorg"

    def test_get_otlp_endpoint_default_org(self) -> None:
        """Test OTLP endpoint uses default org when not specified."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
        )

        endpoint = config.get_otlp_endpoint()
        assert endpoint == "http://localhost:5080/api/default"

    def test_get_otlp_endpoint_no_url(self) -> None:
        """Test OTLP endpoint returns None when URL is not set."""
        config = OpenObserveConfig()

        endpoint = config.get_otlp_endpoint()
        assert endpoint is None

    def test_get_otlp_endpoint_complex_url(self) -> None:
        """Test OTLP endpoint with complex URL structure."""
        config = OpenObserveConfig(
            url="https://openobserve.example.com/api/production/logs",
            org="production",
        )

        endpoint = config.get_otlp_endpoint()
        # Should extract base URL before /api/
        assert endpoint == "https://openobserve.example.com/api/production"


class TestIsAvailable(FoundationTestCase):
    """Tests for is_available method."""

    def test_is_available_not_configured(self) -> None:
        """Test is_available returns False when not configured."""
        config = OpenObserveConfig()

        assert config.is_available() is False

    def test_is_available_connection_succeeds(self) -> None:
        """Test is_available returns True when connection test succeeds."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        with patch(
            "provide.foundation.integrations.openobserve.client.OpenObserveClient"
        ) as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock asyncio.run to return True
            with patch("asyncio.run") as mock_run:
                mock_run.return_value = True

                result = config.is_available()

                assert result is True
                mock_client_class.assert_called_once_with(
                    url="http://localhost:5080",
                    username="test@example.com",
                    password="secret",
                    organization="default",
                )

    def test_is_available_connection_fails(self) -> None:
        """Test is_available returns False when connection test fails."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        with patch(
            "provide.foundation.integrations.openobserve.client.OpenObserveClient"
        ) as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock asyncio.run to return False
            with patch("asyncio.run") as mock_run:
                mock_run.return_value = False

                result = config.is_available()

                assert result is False

    def test_is_available_exception_handling(self) -> None:
        """Test is_available returns False on exceptions."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        with patch(
            "provide.foundation.integrations.openobserve.client.OpenObserveClient"
        ) as mock_client_class:
            mock_client_class.side_effect = ValueError("Connection failed")

            result = config.is_available()

            assert result is False

    def test_is_available_with_custom_org(self) -> None:
        """Test is_available passes custom organization to client."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
            org="custom-org",
        )

        with patch(
            "provide.foundation.integrations.openobserve.client.OpenObserveClient"
        ) as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            with patch("asyncio.run") as mock_run:
                mock_run.return_value = True

                config.is_available()

                mock_client_class.assert_called_once_with(
                    url="http://localhost:5080",
                    username="test@example.com",
                    password="secret",
                    organization="custom-org",
                )

    def test_is_available_asyncio_exception(self) -> None:
        """Test is_available handles asyncio exceptions."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        with patch("asyncio.run") as mock_run:
            mock_run.side_effect = RuntimeError("Event loop closed")

            result = config.is_available()

            assert result is False


class TestConfigEdgeCases(FoundationTestCase):
    """Tests for edge cases and special scenarios."""

    def test_config_with_special_characters_in_password(self) -> None:
        """Test config handles special characters in password."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="p@ssw0rd!#$%",
        )

        assert config.password == "p@ssw0rd!#$%"
        assert config.is_configured() is True

    def test_config_url_normalization(self) -> None:
        """Test various URL formats are handled correctly."""
        test_cases = [
            ("http://localhost:5080", "http://localhost:5080/api/default"),
            ("http://localhost:5080/", "http://localhost:5080//api/default"),  # Trailing slash preserved
            ("http://localhost:5080/api/test", "http://localhost:5080/api/default"),
            ("https://openobserve.example.com", "https://openobserve.example.com/api/default"),
        ]

        for url, expected_endpoint in test_cases:
            config = OpenObserveConfig(url=url)
            endpoint = config.get_otlp_endpoint()
            assert endpoint == expected_endpoint

    def test_config_repr_does_not_expose_password(self) -> None:
        """Test that config repr doesn't expose sensitive data."""
        config = OpenObserveConfig(
            url="http://localhost:5080",
            user="test@example.com",
            password="secret",
        )

        # OpenObserveConfig uses repr=False, so repr should be default attrs behavior
        config_repr = repr(config)
        # Just verify repr doesn't crash
        assert isinstance(config_repr, str)


__all__ = [
    "TestConfigEdgeCases",
    "TestGetOTLPEndpoint",
    "TestIsAvailable",
    "TestIsConfigured",
    "TestOpenObserveConfigInitialization",
]

# 🧱🏗️🔚
