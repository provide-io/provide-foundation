#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OTLP client send_log method.

Tests all log sending functionality including success cases, error handling,
circuit breaker integration, and attribute handling."""

from __future__ import annotations

from provide.testkit.mocking import Mock, patch

from provide.foundation.logger.otlp.client import OTLPLogClient


class TestSendLog:
    """Tests for send_log method."""

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_success(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test successful log sending."""
        # Mock circuit breaker
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        # Mock logger provider
        mock_provider = Mock()
        mock_logger = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_create_provider.return_value = mock_provider

        # Create client with OTLP available
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message", level="INFO")

        assert result is True
        mock_breaker.record_success.assert_called_once()
        mock_logger.emit.assert_called_once()
        mock_provider.force_flush.assert_called_once()
        mock_provider.shutdown.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_send_log_otlp_unavailable(self, mock_get_breaker: Mock) -> None:
        """Test send_log when OTLP is not available."""
        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = False

        result = client.send_log("Test message")

        assert result is False
        mock_get_breaker.assert_not_called()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    def test_send_log_circuit_breaker_open(self, mock_get_breaker: Mock) -> None:
        """Test send_log when circuit breaker is open."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = False
        mock_get_breaker.return_value = mock_breaker

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_provider_creation_fails(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log when provider creation fails."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_provider.return_value = None

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False
        mock_breaker.record_failure.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_with_attributes(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log with custom attributes."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_provider = Mock()
        mock_logger = Mock()
        mock_provider.get_logger.return_value = mock_logger
        mock_create_provider.return_value = mock_provider

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        attributes = {"user_id": "123", "action": "login"}
        result = client.send_log("User logged in", level="INFO", attributes=attributes)

        assert result is True
        mock_logger.emit.assert_called_once()

    @patch("provide.foundation.logger.otlp.client.get_otlp_circuit_breaker")
    @patch("provide.foundation.logger.otlp.client.OTLPLogClient._create_logger_provider_internal")
    def test_send_log_exception(
        self,
        mock_create_provider: Mock,
        mock_get_breaker: Mock,
    ) -> None:
        """Test send_log handles exceptions gracefully."""
        mock_breaker = Mock()
        mock_breaker.can_attempt.return_value = True
        mock_get_breaker.return_value = mock_breaker

        mock_create_provider.side_effect = Exception("Provider error")

        client = OTLPLogClient(endpoint="https://api.example.com")
        client._otlp_available = True

        result = client.send_log("Test message")

        assert result is False
        mock_breaker.record_failure.assert_called_once()

    def test_send_log_without_circuit_breaker(self) -> None:
        """Test send_log when circuit breaker is disabled."""
        client = OTLPLogClient(
            endpoint="https://api.example.com",
            use_circuit_breaker=False,
        )
        client._otlp_available = False

        result = client.send_log("Test message")

        # Should return False due to OTLP unavailable
        assert result is False


# 🧱🏗️🔚
