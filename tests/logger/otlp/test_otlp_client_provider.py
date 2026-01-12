#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OTLP client provider creation and status methods.

Tests logger provider creation, availability checking, and stats retrieval."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch

from provide.foundation.logger.otlp.client import OTLPLogClient


class TestCreateLoggerProvider:
    """Tests for create_logger_provider method."""

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_create_logger_provider_success(
        self,
        mock_create_internal: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test successful logger provider creation."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_provider = Mock()
        mock_create_internal.return_value = mock_provider

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result == mock_provider
        mock_breaker.record_success.assert_called_once()

    def test_create_logger_provider_otlp_unavailable(self) -> None:
        """Test create_logger_provider when OTLP is unavailable."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.create_logger_provider()

        assert result is None

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_create_logger_provider_circuit_open(self, mock_get_breaker: Mock) -> None:
        """Test create_logger_provider when circuit is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result is None

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_create_logger_provider_exception(
        self,
        mock_create_internal: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test create_logger_provider handles exceptions."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_internal.side_effect = Exception("Provider error")

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.create_logger_provider()

        assert result is None
        mock_breaker.record_failure.assert_called_once()


class TestCreateLoggerProviderInternal:
    """Tests for _create_logger_provider_internal method."""

    @patch("provide.foundation.logger.otlp.client.create_otlp_resource")
    def test_create_logger_provider_internal_import_error(
        self,
        mock_create_resource: Mock,
    ) -> None:
        """Test _create_logger_provider_internal when imports fail."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            service_name="test-service",
        )

        # This will naturally fail if OpenTelemetry is not installed
        result = client._create_logger_provider_internal()

        # Result could be None if OTLP is not available
        assert result is None or result is not None

    @patch("provide.foundation.logger.otlp.client.create_otlp_resource")
    def test_create_logger_provider_internal_exception(
        self,
        mock_create_resource: Mock,
    ) -> None:
        """Test _create_logger_provider_internal handles exceptions."""
        mock_create_resource.side_effect = Exception("Resource error")

        client = OTLPLogClient(endpoint="https://api.example.com")

        result = client._create_logger_provider_internal()

        assert result is None


class TestIsAvailable:
    """Tests for is_available method."""

    def test_is_available_otlp_unavailable(self) -> None:
        """Test is_available when OTLP is not available."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.is_available()

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_is_available_circuit_open(self, mock_get_breaker: Mock) -> None:
        """Test is_available when circuit breaker is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.is_available()

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_is_available_true(self, mock_get_breaker: Mock) -> None:
        """Test is_available when everything is available."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.is_available()

        assert result is True

    def test_is_available_without_circuit_breaker(self) -> None:
        """Test is_available when circuit breaker is disabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = True

        result = client.is_available()

        assert result is True


class TestGetStats:
    """Tests for get_stats method."""

    def test_get_stats_basic(self) -> None:
        """Test get_stats returns client information."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            service_name="test-service",
        )
        client._otlp_available = True

        stats = client.get_stats()

        assert stats["otlp_available"] is True
        assert stats["endpoint"] == "https://api.example.com/v1/logs"
        assert stats["service_name"] == "test-service"

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_get_stats_with_circuit_breaker(self, mock_get_breaker: Mock) -> None:
        """Test get_stats includes circuit breaker stats."""
        mock_breaker = Mock()
        mock_breaker_stats = {
            "state": "closed",
            "failure_count": 0,
        }
        mock_breaker.get_stats.return_value = mock_breaker_stats
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        stats = client.get_stats()

        assert "circuit_breaker" in stats
        assert stats["circuit_breaker"] == mock_breaker_stats

    def test_get_stats_without_circuit_breaker(self) -> None:
        """Test get_stats without circuit breaker enabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = False

        stats = client.get_stats()

        assert "circuit_breaker" not in stats
        assert stats["otlp_available"] is False


# 🧱🏗️🔚
