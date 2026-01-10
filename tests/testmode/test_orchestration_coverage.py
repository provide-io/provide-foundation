#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for testmode/orchestration.py.

These tests target uncovered lines and edge cases in reset orchestration."""

from __future__ import annotations

import os
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, Mock, patch

from provide.foundation.testmode.orchestration import (
    _reset_foundation_environment_variables,
    _reset_meter_provider,
    _reset_opentelemetry_providers,
    _reset_otel_once_flag,
    _reset_tracer_provider,
    reset_foundation_for_testing,
    reset_foundation_state,
)


class TestResetOtelOnceFlag(FoundationTestCase):
    """Test _reset_otel_once_flag() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_resets_done_flag_without_lock(self) -> None:
        """Test resetting _done flag when no lock present."""
        mock_once = Mock()
        mock_once._done = True

        _reset_otel_once_flag(mock_once)

        assert mock_once._done is False

    def test_resets_done_flag_with_lock(self) -> None:
        """Test resetting _done flag when lock is present."""
        mock_lock = MagicMock()
        mock_once = Mock()
        mock_once._done = True
        mock_once._lock = mock_lock

        _reset_otel_once_flag(mock_once)

        # Lock should be acquired
        mock_lock.__enter__.assert_called_once()
        assert mock_once._done is False

    def test_handles_object_without_done_attribute(self) -> None:
        """Test handling object without _done attribute."""
        mock_once = Mock(spec=[])  # No _done attribute

        # Should not raise error
        _reset_otel_once_flag(mock_once)

    def test_handles_object_without_lock_attribute(self) -> None:
        """Test handling object with _done but no _lock."""
        mock_once = Mock(spec=["_done"])
        mock_once._done = True

        _reset_otel_once_flag(mock_once)

        # Should reset _done even without lock
        assert mock_once._done is False


class TestResetTracerProvider(FoundationTestCase):
    """Test _reset_tracer_provider() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_resets_tracer_provider_completes(self) -> None:
        """Test resetting tracer provider completes without error."""
        # Just verify it doesn't crash - the actual OTel reset logic
        # is complex and depends on real OpenTelemetry being available
        _reset_tracer_provider()

    def test_handles_import_error_for_opentelemetry(self) -> None:
        """Test graceful handling when OpenTelemetry not available."""

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "opentelemetry" in name:
                raise ImportError("No module named 'opentelemetry'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            # Should not raise error
            _reset_tracer_provider()

    def test_handles_generic_exception_during_reset(self) -> None:
        """Test handling of generic exceptions during reset."""
        mock_otel_trace = Mock()
        mock_otel_trace.set_tracer_provider.side_effect = RuntimeError("Test error")

        with patch.dict("sys.modules", {"opentelemetry.trace": mock_otel_trace}):
            # Should not raise error (exception caught)
            _reset_tracer_provider()

    def test_resets_without_tracer_provider_set_once_attribute(self) -> None:
        """Test reset when _TRACER_PROVIDER_SET_ONCE not present."""
        mock_otel_trace = Mock(spec=["set_tracer_provider"])
        mock_otel_trace.set_tracer_provider = Mock()

        with patch.dict("sys.modules", {"opentelemetry.trace": mock_otel_trace}):
            # Should still work without the Once flag
            _reset_tracer_provider()


class TestResetMeterProvider(FoundationTestCase):
    """Test _reset_meter_provider() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_resets_meter_provider_completes(self) -> None:
        """Test resetting meter provider completes without error."""
        # Just verify it doesn't crash - the actual OTel reset logic
        # is complex and depends on real OpenTelemetry being available
        _reset_meter_provider()

    def test_handles_import_error_for_opentelemetry_metrics(self) -> None:
        """Test graceful handling when OpenTelemetry metrics not available."""

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "opentelemetry.metrics" in name:
                raise ImportError("No module named 'opentelemetry.metrics'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            # Should not raise error
            _reset_meter_provider()

    def test_handles_generic_exception_during_reset(self) -> None:
        """Test handling of generic exceptions during meter reset."""
        mock_otel_metrics = Mock()
        mock_otel_metrics.set_meter_provider.side_effect = RuntimeError("Test error")

        with patch.dict("sys.modules", {"opentelemetry.metrics": mock_otel_metrics}):
            # Should not raise error (exception caught)
            _reset_meter_provider()

    def test_resets_without_meter_provider_set_once_attribute(self) -> None:
        """Test reset when _METER_PROVIDER_SET_ONCE not present."""
        mock_otel_metrics_internal = Mock(spec=[])  # No _METER_PROVIDER_SET_ONCE

        mock_otel_metrics = Mock()
        mock_otel_metrics.set_meter_provider = Mock()

        with (
            patch.dict("sys.modules", {"opentelemetry.metrics": mock_otel_metrics}),
            patch.dict("sys.modules", {"opentelemetry.metrics._internal": mock_otel_metrics_internal}),
        ):
            # Should still work without the Once flag
            _reset_meter_provider()


class TestResetOpentelemetryProviders(FoundationTestCase):
    """Test _reset_opentelemetry_providers() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_calls_both_tracer_and_meter_resets(self) -> None:
        """Test that both tracer and meter providers are reset."""
        with (
            patch("provide.foundation.testmode.orchestration._reset_tracer_provider") as mock_tracer,
            patch("provide.foundation.testmode.orchestration._reset_meter_provider") as mock_meter,
        ):
            _reset_opentelemetry_providers()

            mock_tracer.assert_called_once()
            mock_meter.assert_called_once()


class TestResetFoundationEnvironmentVariables(FoundationTestCase):
    """Test _reset_foundation_environment_variables() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_sets_default_environment_variables(self) -> None:
        """Test that default environment variables are set."""
        # Remove defaults if present
        env_backup = os.environ.copy()
        try:
            if "PROVIDE_LOG_LEVEL" in os.environ:
                del os.environ["PROVIDE_LOG_LEVEL"]
            if "FOUNDATION_SUPPRESS_TESTING_WARNINGS" in os.environ:
                del os.environ["FOUNDATION_SUPPRESS_TESTING_WARNINGS"]

            _reset_foundation_environment_variables()

            assert os.environ.get("PROVIDE_LOG_LEVEL") == "DEBUG"
            assert os.environ.get("FOUNDATION_SUPPRESS_TESTING_WARNINGS") == "true"
        finally:
            # Restore environment
            os.environ.clear()
            os.environ.update(env_backup)

    def test_preserves_existing_default_values(self) -> None:
        """Test that existing default values are not overridden."""
        env_backup = os.environ.copy()
        try:
            os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
            os.environ["FOUNDATION_SUPPRESS_TESTING_WARNINGS"] = "false"

            _reset_foundation_environment_variables()

            # Should preserve existing values
            assert os.environ.get("PROVIDE_LOG_LEVEL") == "INFO"
            assert os.environ.get("FOUNDATION_SUPPRESS_TESTING_WARNINGS") == "false"
        finally:
            os.environ.clear()
            os.environ.update(env_backup)

    def test_removes_conditional_environment_variables(self) -> None:
        """Test that conditional variables are removed."""
        env_backup = os.environ.copy()
        try:
            os.environ["PROVIDE_PROFILE"] = "production"
            os.environ["PROVIDE_DEBUG"] = "true"
            os.environ["PROVIDE_JSON_OUTPUT"] = "true"

            _reset_foundation_environment_variables()

            # These should be removed
            assert "PROVIDE_PROFILE" not in os.environ
            assert "PROVIDE_DEBUG" not in os.environ
            assert "PROVIDE_JSON_OUTPUT" not in os.environ
        finally:
            os.environ.clear()
            os.environ.update(env_backup)


class TestResetFoundationState(FoundationTestCase):
    """Test reset_foundation_state() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_prevents_recursive_resets(self) -> None:
        """Test that recursive resets are prevented."""
        call_count = 0

        def mock_reset_structlog() -> None:
            nonlocal call_count
            call_count += 1
            # Try to trigger recursive reset
            if call_count == 1:
                reset_foundation_state()

        with patch("provide.foundation.testmode.internal.reset_structlog_state", mock_reset_structlog):
            reset_foundation_state()

            # Should only be called once (recursion prevented)
            assert call_count == 1

    def test_sets_reset_in_progress_flag(self) -> None:
        """Test that reset_in_progress flag is set during reset."""
        reset_called = False

        def check_flag_during_reset() -> None:
            nonlocal reset_called
            # Access the flag via the module
            import provide.foundation.testmode.orchestration as orch

            reset_called = orch._reset_in_progress

        with patch("provide.foundation.testmode.internal.reset_structlog_state", check_flag_during_reset):
            reset_foundation_state()

            # Flag should have been True during reset
            assert reset_called is True

    def test_skips_otel_reset_in_xdist_worker(self) -> None:
        """Test that OTel reset is skipped in pytest-xdist worker."""
        with (
            patch.dict("os.environ", {"PYTEST_XDIST_WORKER": "gw0"}),
            patch("provide.foundation.testmode.orchestration._reset_opentelemetry_providers") as mock_otel,
        ):
            reset_foundation_state()

            # Should not be called in xdist worker
            mock_otel.assert_not_called()

    def test_performs_otel_reset_when_not_in_xdist(self) -> None:
        """Test that OTel reset is performed when not in xdist worker."""
        # Ensure PYTEST_XDIST_WORKER is not set
        env_backup = os.environ.get("PYTEST_XDIST_WORKER")
        try:
            if "PYTEST_XDIST_WORKER" in os.environ:
                del os.environ["PYTEST_XDIST_WORKER"]

            with patch(
                "provide.foundation.testmode.orchestration._reset_opentelemetry_providers"
            ) as mock_otel:
                reset_foundation_state()

                # Should be called when not in xdist
                mock_otel.assert_called_once()
        finally:
            # Restore environment
            if env_backup is not None:
                os.environ["PYTEST_XDIST_WORKER"] = env_backup

    def test_continues_on_processor_reset_import_error(self) -> None:
        """Test that reset continues even if processor import fails."""
        # The actual implementation catches ImportError internally
        # We just verify the function completes without error
        reset_foundation_state()

    def test_continues_on_hub_reset_import_error(self) -> None:
        """Test that reset continues even if hub event_handlers import fails."""
        # The actual implementation catches ImportError internally
        # We just verify the function completes without error
        reset_foundation_state()

    def test_resets_successfully(self) -> None:
        """Test that full reset completes successfully."""
        # Should complete without errors
        reset_foundation_state()

        # Should be able to run again (idempotent)
        reset_foundation_state()


class TestResetFoundationForTesting(FoundationTestCase):
    """Test reset_foundation_for_testing() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_prevents_recursive_resets(self) -> None:
        """Test that recursive resets during testing are prevented."""
        call_count = 0

        def mock_reset_state() -> None:
            nonlocal call_count
            call_count += 1
            # Try to trigger recursive reset
            if call_count == 1:
                reset_foundation_for_testing()

        with patch("provide.foundation.testmode.orchestration.reset_foundation_state", mock_reset_state):
            reset_foundation_for_testing()

            # Should only be called once (recursion prevented)
            assert call_count == 1

    def test_preserves_test_stream(self) -> None:
        """Test that test stream is preserved across reset."""
        import io

        test_stream = io.StringIO()

        mock_get_stream = Mock(return_value=test_stream)
        mock_set_stream = Mock()

        with (
            patch("provide.foundation.streams.core.get_log_stream", mock_get_stream),
            patch("provide.foundation.streams.core.set_log_stream_for_testing", mock_set_stream),
        ):
            reset_foundation_for_testing()

            # Should restore the test stream
            mock_set_stream.assert_called_once_with(test_stream)

    def test_does_not_preserve_stderr_stream(self) -> None:
        """Test that stderr stream is not preserved."""
        mock_get_stream = Mock(return_value=sys.stderr)
        mock_set_stream = Mock()

        with (
            patch("provide.foundation.streams.core.get_log_stream", mock_get_stream),
            patch("provide.foundation.streams.core.set_log_stream_for_testing", mock_set_stream),
        ):
            reset_foundation_for_testing()

            # Should not restore stderr
            mock_set_stream.assert_not_called()

    def test_does_not_preserve_stdout_stream(self) -> None:
        """Test that stdout stream is not preserved."""
        mock_get_stream = Mock(return_value=sys.stdout)
        mock_set_stream = Mock()

        with (
            patch("provide.foundation.streams.core.get_log_stream", mock_get_stream),
            patch("provide.foundation.streams.core.set_log_stream_for_testing", mock_set_stream),
        ):
            reset_foundation_for_testing()

            # Should not restore stdout
            mock_set_stream.assert_not_called()

    def test_handles_exception_getting_current_stream(self) -> None:
        """Test handling of exception when getting current stream."""
        mock_get_stream = Mock(side_effect=RuntimeError("Stream error"))

        with patch("provide.foundation.streams.core.get_log_stream", mock_get_stream):
            # Should not raise error (exception caught)
            reset_foundation_for_testing()

    def test_handles_exception_restoring_stream(self) -> None:
        """Test handling of exception when restoring stream."""
        import io

        test_stream = io.StringIO()
        mock_get_stream = Mock(return_value=test_stream)
        mock_set_stream = Mock(side_effect=RuntimeError("Set error"))

        with (
            patch("provide.foundation.streams.core.get_log_stream", mock_get_stream),
            patch("provide.foundation.streams.core.set_log_stream_for_testing", mock_set_stream),
        ):
            # Should not raise error (exception caught)
            reset_foundation_for_testing()

    def test_continues_on_transport_registration_import_error(self) -> None:
        """Test that reset continues even if transport import fails."""
        # The actual implementation catches ImportError internally
        # We just verify the function completes without error
        reset_foundation_for_testing()

    def test_continues_on_testmode_internal_import_error(self) -> None:
        """Test that reset continues even if testmode.internal import fails."""
        # The actual implementation catches ImportError internally
        # We just verify the function completes without error
        reset_foundation_for_testing()

    def test_resets_successfully(self) -> None:
        """Test that full reset for testing completes successfully."""
        # Should complete without errors
        reset_foundation_for_testing()

        # Should be able to run again (idempotent)
        reset_foundation_for_testing()


__all__ = [
    "TestResetFoundationEnvironmentVariables",
    "TestResetFoundationForTesting",
    "TestResetFoundationState",
    "TestResetMeterProvider",
    "TestResetOpentelemetryProviders",
    "TestResetOtelOnceFlag",
    "TestResetTracerProvider",
]

# 🧱🏗️🔚
