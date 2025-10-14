from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

"""Simplified tests for OpenObserve OTLP integration module.

Tests focus on the fallback logic between OTLP and bulk API.
Detailed OTLP tests are in test_otlp_adapter.py and logger/otlp/ tests.
"""


class TestSendLog(FoundationTestCase):
    """Test send_log function (main entry point with fallback logic)."""

    def test_send_log_prefer_otlp_success(self) -> None:
        """Test send_log tries OTLP first when preferred."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        # Mock successful OTLP client
        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.send_log.return_value = True

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_from_env.return_value = mock_client

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_client.send_log.assert_called_once_with("Test message", "INFO", None)
            mock_bulk.assert_not_called()

    def test_send_log_otlp_fails_fallback_to_bulk(self) -> None:
        """Test send_log falls back to bulk API when OTLP fails."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        # Mock OTLP client that fails
        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.send_log.return_value = False  # OTLP fails

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_from_env.return_value = mock_client
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_client.send_log.assert_called_once()
            mock_bulk.assert_called_once_with("Test message", "INFO", None, None, None)

    def test_send_log_otlp_unavailable_fallback_to_bulk(self) -> None:
        """Test send_log uses bulk API when OTLP client unavailable."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        # Mock OTLP client that's not available
        mock_client = Mock()
        mock_client.is_available.return_value = False

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_from_env.return_value = mock_client
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_client.send_log.assert_not_called()  # Not called because unavailable
            mock_bulk.assert_called_once()

    def test_send_log_no_client_fallback_to_bulk(self) -> None:
        """Test send_log uses bulk API when OTLP client creation fails."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_from_env.return_value = None  # Client creation fails
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=True)

            assert result is True
            mock_bulk.assert_called_once()

    def test_send_log_prefer_bulk_skips_otlp(self) -> None:
        """Test send_log skips OTLP when prefer_otlp=False."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_bulk.return_value = True

            result = send_log("Test message", prefer_otlp=False)

            assert result is True
            mock_from_env.assert_not_called()  # OTLP not attempted
            mock_bulk.assert_called_once()

    def test_send_log_with_service_name(self) -> None:
        """Test send_log passes service_name parameter correctly."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.send_log.return_value = False  # Force fallback to test bulk API

        with (
            patch(
                "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
            ) as mock_from_env,
            patch("provide.foundation.integrations.openobserve.otlp.send_log_bulk") as mock_bulk,
        ):
            mock_from_env.return_value = mock_client
            mock_bulk.return_value = True

            result = send_log("Test message", service_name="my-service")

            assert result is True
            # Verify service_name passed to bulk API
            mock_bulk.assert_called_once_with("Test message", "INFO", "my-service", None, None)

    def test_send_log_with_attributes(self) -> None:
        """Test send_log passes attributes correctly."""
        from provide.foundation.integrations.openobserve.otlp import send_log

        mock_client = Mock()
        mock_client.is_available.return_value = True
        mock_client.send_log.return_value = True

        with patch(
            "provide.foundation.integrations.openobserve.otlp.OpenObserveOTLPClient.from_env"
        ) as mock_from_env:
            mock_from_env.return_value = mock_client

            attrs = {"user_id": 123, "action": "login"}
            result = send_log("User logged in", level="INFO", attributes=attrs)

            assert result is True
            mock_client.send_log.assert_called_once_with("User logged in", "INFO", attrs)


class TestModuleStructure(FoundationTestCase):
    """Test basic module structure and imports."""

    def test_module_imports_correctly(self) -> None:
        """Test that module can be imported without errors."""
        import provide.foundation.integrations.openobserve.otlp as otlp_module

        assert hasattr(otlp_module, "send_log")
        # Verify removed functions are gone
        assert not hasattr(otlp_module, "send_log_otlp")
        assert not hasattr(otlp_module, "create_otlp_logger_provider")
        # send_log_bulk is imported for internal use, not exposed in __all__

    def test_send_log_in_all(self) -> None:
        """Test that send_log is exported in __all__."""
        from provide.foundation.integrations.openobserve.otlp import __all__

        assert "send_log" in __all__
        assert len(__all__) == 1  # Only send_log should be exported
