#
# tests/test_logger_base.py
#
"""
Unit tests for src.pyvider.telemetry.logger.base.py
"""
import io
import sys
import threading
from unittest.mock import MagicMock, patch

import structlog

# For resetting global state consistently
from pyvider.telemetry.core import reset_pyvider_setup_for_testing

# Functions/classes/variables to test from logger/base.py
from pyvider.telemetry.logger.base import (
    _LAZY_SETUP_STATE,
    PyviderLogger,
    _get_safe_stderr,
    logger as global_pyvider_logger,
)


class TestGetSafeStderrBase:
    def test_get_safe_stderr_is_valid_in_base(self) -> None:
        original_stderr = sys.stderr
        if original_stderr is None:
            sys.stderr = io.StringIO("temp stderr for base test")
        try:
            stream = _get_safe_stderr()
            assert stream == sys.stderr
        finally:
            if original_stderr is None and hasattr(sys, 'stderr'):
                 sys.stderr = original_stderr

    def test_get_safe_stderr_is_none_in_base(self) -> None:
        with patch.object(sys, 'stderr', None):
            fallback_stream = _get_safe_stderr()
            assert isinstance(fallback_stream, io.StringIO)


class TestEnsureConfiguredErrorPath:
    def test_ensure_configured_uses_fallback_if_previous_error(self, capsys) -> None:
        reset_pyvider_setup_for_testing()
        class FirstAttemptError(Exception):
            pass
        perform_lazy_setup_mock = MagicMock(side_effect=FirstAttemptError("First setup attempt failed"))
        emergency_fallback_mock = MagicMock()
        test_logger = PyviderLogger()

        with patch.object(PyviderLogger, '_perform_lazy_setup', perform_lazy_setup_mock), \
             patch.object(PyviderLogger, '_setup_emergency_fallback', emergency_fallback_mock):

            test_logger.info("First log attempt - triggers failing setup")

            perform_lazy_setup_mock.assert_called_once()
            assert isinstance(_LAZY_SETUP_STATE["error"], FirstAttemptError)
            assert _LAZY_SETUP_STATE["done"] is False
            assert emergency_fallback_mock.call_count >= 1
            initial_fallback_call_count = emergency_fallback_mock.call_count

            test_logger.info("Second log attempt - should use fallback")

            perform_lazy_setup_mock.assert_called_once()
            assert emergency_fallback_mock.call_count > initial_fallback_call_count
        reset_pyvider_setup_for_testing()


class TestEnsureConfiguredReturnLoggerFactoryExceptionPath:
    def test_ensure_configured_handles_exception_in_rtlf_check(self, capsys) -> None:
        reset_pyvider_setup_for_testing()
        with patch('structlog.get_config', side_effect=RuntimeError("Simulated error in get_config")):
            perform_lazy_setup_mock = MagicMock()
            emergency_fallback_mock = MagicMock()
            test_logger = PyviderLogger()
            with patch.object(PyviderLogger, '_perform_lazy_setup', perform_lazy_setup_mock), \
                 patch.object(PyviderLogger, '_setup_emergency_fallback', emergency_fallback_mock):
                test_logger.info("Log attempt when get_config fails")
                perform_lazy_setup_mock.assert_called_once()
                assert _LAZY_SETUP_STATE["error"] is None
                assert _LAZY_SETUP_STATE["done"] is True
                emergency_fallback_mock.assert_not_called()
        reset_pyvider_setup_for_testing()


class TestEnsureConfiguredReturnLoggerFactoryPath:
    def test_ensure_configured_handles_returnloggerfactory(self, capsys) -> None:
        reset_pyvider_setup_for_testing()
        structlog.configure(logger_factory=structlog.ReturnLoggerFactory())
        perform_lazy_setup_mock = MagicMock()
        test_logger = PyviderLogger()
        with patch.object(PyviderLogger, '_perform_lazy_setup', perform_lazy_setup_mock):
            test_logger.info("Log attempt when ReturnLoggerFactory is active")
        perform_lazy_setup_mock.assert_not_called()
        assert _LAZY_SETUP_STATE["done"] is True
        assert _LAZY_SETUP_STATE["error"] is None
        reset_pyvider_setup_for_testing()


class TestEnsureConfiguredPerformLazySetupFails:
    def test_ensure_configured_main_exception_path(self, capsys) -> None:
        reset_pyvider_setup_for_testing()
        class PerformLazySetupTestError(Exception):
            pass
        perform_lazy_setup_mock = MagicMock(side_effect=PerformLazySetupTestError("Setup failed!"))
        emergency_fallback_mock = MagicMock()

        with patch.object(PyviderLogger, '_perform_lazy_setup', perform_lazy_setup_mock), \
             patch.object(PyviderLogger, '_setup_emergency_fallback', emergency_fallback_mock):
            global_pyvider_logger.error("Test log to trigger failing lazy setup")
            perform_lazy_setup_mock.assert_called_once()
            assert isinstance(_LAZY_SETUP_STATE["error"], PerformLazySetupTestError)
            assert str(_LAZY_SETUP_STATE["error"]) == "Setup failed!"
            assert _LAZY_SETUP_STATE["done"] is False
            assert emergency_fallback_mock.call_count >= 1
        reset_pyvider_setup_for_testing()


class TestReentrancyHandling:
    def test_ensure_configured_handles_reentrant_call_via_in_progress_flag(self, capsys) -> None:
        """
        Tests that if _ensure_configured is called re-entrantly while setup is in progress,
        the emergency fallback is triggered. This covers the `if _LAZY_SETUP_STATE["in_progress"]:`
        checks (lines ~90 and ~124).
        """
        reset_pyvider_setup_for_testing()

        # Use the global logger instance
        logger_instance = global_pyvider_logger

        # Simple mock for _setup_emergency_fallback, we only care if it's called
        emergency_fallback_mock = MagicMock()

        re_entrant_call_made_event = threading.Event()

        # This counter ensures that the re-entrant call is made only once
        # by the mock, to prevent actual infinite recursion in the test itself.
        perform_lazy_setup_call_count = 0

        def mock_perform_lazy_setup(self_arg) -> None:
            nonlocal perform_lazy_setup_call_count
            perform_lazy_setup_call_count += 1

            # Simulate that _ensure_configured has set "in_progress" to True before calling this
            # For this test, we rely on the outer _ensure_configured to have set it.

            if perform_lazy_setup_call_count == 1: # Only on the first call from outer _ensure_configured
                # Make the re-entrant call
                logger_instance.info("Re-entrant log during setup")
                re_entrant_call_made_event.set() # Signal that re-entrant call has been made

            # Simplified mock: does not attempt to complete original setup fully for this test.
            # We're focused on the re-entrancy mechanism.

        # Patch _setup_emergency_fallback on the class to track calls
        with patch.object(PyviderLogger, '_setup_emergency_fallback', emergency_fallback_mock), \
             patch.object(PyviderLogger, '_perform_lazy_setup', mock_perform_lazy_setup):

            logger_instance.info("Initial logging call") # This triggers the first _ensure_configured

            # Assertions
            assert re_entrant_call_made_event.is_set(), "Re-entrant call was not made by mock_perform_lazy_setup"

            assert emergency_fallback_mock.call_count >= 1, \
                "Expected emergency_fallback to be called at least once by re-entrant call."

        reset_pyvider_setup_for_testing()
