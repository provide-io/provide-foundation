#
# tests/test_core.py
#
"""
Unit tests for src.pyvider.telemetry.core.py
"""
import io
import logging as stdlib_logging
import sys
from unittest.mock import MagicMock, patch

import pytest
from pytest import CaptureFixture  # Added for capsys
import structlog  # Added for teardown_method in TestHandleGloballyDisabledSetup

from pyvider.telemetry.config import (
    LoggingConfig,
    TelemetryConfig,
)

# Functions to test from core.py
from pyvider.telemetry.core import (
    _CORE_SETUP_LOGGER_NAME,
    _create_core_setup_logger,
    _get_safe_stderr,
    reset_pyvider_setup_for_testing,  # For coverage of _LAZY_SETUP_STATE reset
    setup_telemetry,  # For coverage of _LAZY_SETUP_STATE reset
    shutdown_pyvider_telemetry,  # For coverage of shutdown message
)

# To interact with _LAZY_SETUP_STATE for reset coverage checks
from pyvider.telemetry.logger import base as logger_base_module


class TestGetSafeStderr:
    def test_get_safe_stderr_is_none(self) -> None:
        """
        Tests that _get_safe_stderr returns an io.StringIO when sys.stderr is None.
        """
        with patch.object(sys, 'stderr', None):
            fallback_stream = _get_safe_stderr()
            assert isinstance(fallback_stream, io.StringIO), \
                "Fallback stream should be an io.StringIO instance when sys.stderr is None."

    def test_get_safe_stderr_is_valid(self) -> None:
        """
        Tests that _get_safe_stderr returns sys.stderr when it is valid.
        """
        original_stderr = sys.stderr
        # Ensure sys.stderr is something valid, not None, for this test
        if original_stderr is None: # Should not happen in normal pytest run
            sys.stderr = io.StringIO("temp stderr for test")

        try:
            # Python's type system can be tricky with sys.stderr if it's None.
            # If sys.stderr could be None, TextIO is not strictly correct.
            # However, _get_safe_stderr handles it.
            if sys.stderr is not None: # Make type checker happy
                stream = _get_safe_stderr()
                assert stream == sys.stderr, \
                    "Should return original sys.stderr when it's valid."
            else: # pragma: no cover (should not be hit if sys.stderr is restored or was not None)
                pytest.skip("sys.stderr was None, cannot run this specific path meaningfully without complex restore.")
        finally:
            if original_stderr is None and hasattr(sys, 'stderr'): # Restore if we changed it
                 sys.stderr = original_stderr

# Placeholder for next tests
class TestCreateCoreSetupLogger:
    def test_create_core_setup_logger_handler_close_exception(self) -> None:
        """
        Tests that _create_core_setup_logger handles exceptions when trying to close
        a pre-existing handler that is not stdout/stderr.
        """
        logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)

        # Store original handlers and level to restore later
        original_handlers = list(logger.handlers)
        original_level = logger.level
        original_propagate = logger.propagate
        logger.handlers.clear() # Clear for a clean slate

        mock_handler_stream = io.StringIO() # A stream that's not stdout/stderr
        mock_handler = stdlib_logging.StreamHandler(mock_handler_stream)
        mock_handler.name = "MockHandlerToClose"
        mock_handler.close = MagicMock(side_effect=RuntimeError("Failed to close"))

        logger.addHandler(mock_handler)

        try:
            # Call the function under test
            # It should catch the RuntimeError from mock_handler.close() and proceed
            _create_core_setup_logger(globally_disabled=False)

            # Assert that the mock_handler was removed (as part of the process)
            # and a new handler (StreamHandler to stderr) was added.
            assert mock_handler not in logger.handlers
            assert len(logger.handlers) == 1
            assert isinstance(logger.handlers[0], stdlib_logging.StreamHandler)
            assert logger.handlers[0].stream == sys.stderr

        except Exception as e: # pragma: no cover
            pytest.fail(f"_create_core_setup_logger raised an unhandled exception: {e!r}")
        finally:
            # Restore logger state
            logger.handlers.clear()
            for handler in original_handlers:
                logger.addHandler(handler)
            logger.setLevel(original_level)
            logger.propagate = original_propagate
            # Ensure the mock stream is closed if it wasn't by the code (it shouldn't be here)
            if not mock_handler_stream.closed:
                mock_handler_stream.close()


class TestStateResetCoverage:
    def test_reset_pyvider_setup_for_testing_resets_lazy_state(self) -> None:
        """
        Ensures reset_pyvider_setup_for_testing correctly resets _LAZY_SETUP_STATE.
        """
        # Set some dummy initial state to ensure it changes
        logger_base_module._LAZY_SETUP_STATE["done"] = True
        logger_base_module._LAZY_SETUP_STATE["error"] = Exception("dummy error")
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = True

        reset_pyvider_setup_for_testing()

        assert not logger_base_module._LAZY_SETUP_STATE["done"]
        assert logger_base_module._LAZY_SETUP_STATE["error"] is None
        assert not logger_base_module._LAZY_SETUP_STATE["in_progress"]

    def test_setup_telemetry_resets_lazy_state(self) -> None:
        """
        Ensures setup_telemetry correctly resets _LAZY_SETUP_STATE before applying config.
        """
        # Set some dummy initial state
        logger_base_module._LAZY_SETUP_STATE["done"] = True
        logger_base_module._LAZY_SETUP_STATE["error"] = Exception("dummy error")
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = True

        # Call setup_telemetry with a basic config
        # This should first reset the _LAZY_SETUP_STATE
        # then set 'done' to True as part of successful setup.
        basic_config = TelemetryConfig(logging=LoggingConfig(default_level="INFO"))
        setup_telemetry(basic_config)

        # After setup_telemetry, "done" should be True, error None, in_progress False
        assert logger_base_module._LAZY_SETUP_STATE["done"]
        assert logger_base_module._LAZY_SETUP_STATE["error"] is None
        assert not logger_base_module._LAZY_SETUP_STATE["in_progress"]

        # Call reset again to clean up for other tests
        reset_pyvider_setup_for_testing()


class TestShutdownCoverage:
    @pytest.mark.asyncio # Mark as an async test
    async def test_shutdown_pyvider_telemetry_logs_message(self, capsys: CaptureFixture[str]) -> None:
        """
        Ensures shutdown_pyvider_telemetry logs its shutdown message.
        This test helps cover line 286 in core.py.
        """
        # Ensure the _core_setup_logger is at a level that allows INFO messages.
        # _create_core_setup_logger defaults to INFO, so this should be fine,
        # but we can explicitly re-call it if needed or adjust the logger.
        # For simplicity, we assume default setup allows INFO.
        # If this test fails to see the message, we might need to force logger reconfig.

        # Call reset to ensure clean state for the logger being tested
        reset_pyvider_setup_for_testing()

        # The _core_setup_logger is configured by reset_pyvider_setup_for_testing
        # to have a stderr handler and INFO level by default.
        # Explicitly ensure level for this test if there's doubt
        core_logger_for_shutdown_test = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)
        original_core_level_for_shutdown = core_logger_for_shutdown_test.level
        core_logger_for_shutdown_test.setLevel(stdlib_logging.INFO) # Ensure INFO is enabled


        await shutdown_pyvider_telemetry()

        # Restore level
        core_logger_for_shutdown_test.setLevel(original_core_level_for_shutdown)

        captured = capsys.readouterr()
        # The message is logged by _core_setup_logger, which has a specific format.
        # Example: "[Pyvider Setup] INFO (pyvider.telemetry.core_setup): 🔌➡️🏁 Pyvider telemetry shutdown called."
        assert "Pyvider telemetry shutdown called" in captured.err
        assert "[Pyvider Setup] INFO (pyvider.telemetry.core_setup):" in captured.err
        assert "🔌➡️🏁" in captured.err


class TestCreateFailsafeHandler:
    def test_create_failsafe_handler_returns_configured_handler(self) -> None:
        """
        Tests that _create_failsafe_handler returns a StreamHandler
        configured with the expected formatter and stream.
        This covers lines 71-75.
        """
        from pyvider.telemetry.core import (
            _create_failsafe_handler,  # Import here as it's private-like
        )

        handler = _create_failsafe_handler()

        assert isinstance(handler, stdlib_logging.StreamHandler), \
            "Handler should be a StreamHandler instance."
        assert handler.stream == sys.stderr, \
            "Handler stream should be sys.stderr."

        assert handler.formatter is not None, "Handler should have a formatter."
        # Test the formatter by formatting a dummy record
        dummy_record = stdlib_logging.LogRecord(
            name="test", level=stdlib_logging.WARNING, pathname="test.py", lineno=1,
            msg="Failsafe test message", args=(), exc_info=None, func="test_func"
        )
        formatted_msg = handler.formatter.format(dummy_record)
        assert formatted_msg == "[Pyvider Failsafe] WARNING: Failsafe test message", \
            "Formatter output does not match expected failsafe format."


class TestEnsureStderrDefault:
    def test_ensure_stderr_default_corrects_stdout(self) -> None:
        """
        Tests that _ensure_stderr_default changes _PYVIDER_LOG_STREAM to sys.stderr
        if it was sys.stdout.
        """
        # Import the global stream variable and the function to test
        from pyvider.telemetry.core import _PYVIDER_LOG_STREAM, _ensure_stderr_default

        original_stream = _PYVIDER_LOG_STREAM

        try:
            # Set the stream to sys.stdout
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', sys.stdout):
                # Call the function
                _ensure_stderr_default()
                # Assert that the stream is now sys.stderr
                # Need to check the actual global variable, not the mock_stream_global which is just a patch context
                from pyvider.telemetry.core import (
                    _PYVIDER_LOG_STREAM as MODIFIED_PYVIDER_LOG_STREAM,
                )
                assert sys.stderr == MODIFIED_PYVIDER_LOG_STREAM
        finally:
            # Restore the original stream value by patching it back
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', original_stream):
                pass # Just to ensure the patch is applied and then reverted

    def test_ensure_stderr_default_leaves_stderr(self) -> None:
        """
        Tests that _ensure_stderr_default leaves _PYVIDER_LOG_STREAM as sys.stderr
        if it already is.
        """
        from pyvider.telemetry.core import _PYVIDER_LOG_STREAM, _ensure_stderr_default
        original_stream = _PYVIDER_LOG_STREAM

        try:
            # Set the stream to sys.stderr
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', sys.stderr):
                _ensure_stderr_default()
                from pyvider.telemetry.core import (
                    _PYVIDER_LOG_STREAM as MODIFIED_PYVIDER_LOG_STREAM,
                )
                assert sys.stderr == MODIFIED_PYVIDER_LOG_STREAM
        finally:
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', original_stream):
                pass

    def test_ensure_stderr_default_leaves_custom_stream(self) -> None:
        """
        Tests that _ensure_stderr_default leaves _PYVIDER_LOG_STREAM as a custom stream
        if it's not sys.stdout.
        """
        from pyvider.telemetry.core import _PYVIDER_LOG_STREAM, _ensure_stderr_default
        original_stream = _PYVIDER_LOG_STREAM
        custom_stream = io.StringIO()

        try:
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', custom_stream):
                _ensure_stderr_default()
                from pyvider.telemetry.core import (
                    _PYVIDER_LOG_STREAM as MODIFIED_PYVIDER_LOG_STREAM,
                )
                assert custom_stream == MODIFIED_PYVIDER_LOG_STREAM
        finally:
            with patch('pyvider.telemetry.core._PYVIDER_LOG_STREAM', original_stream):
                pass
            custom_stream.close()


class TestHandleGloballyDisabledSetup:
    def setup_method(self) -> None:
        # Ensure a clean state for the temp logger before each test
        self.core_setup_logger_name = _CORE_SETUP_LOGGER_NAME
        self.temp_logger_name = f"{self.core_setup_logger_name}_temp_disabled_msg"
        self.temp_logger = stdlib_logging.getLogger(self.temp_logger_name)
        self.original_temp_handlers = list(self.temp_logger.handlers)
        self.original_temp_level = self.temp_logger.level
        self.original_temp_propagate = self.temp_logger.propagate
        self.temp_logger.handlers.clear()

    def teardown_method(self) -> None:
        # Restore original state of the temp logger
        self.temp_logger.handlers.clear()
        for handler in self.original_temp_handlers:
            self.temp_logger.addHandler(handler)
        self.temp_logger.setLevel(self.original_temp_level)
        self.temp_logger.propagate = self.original_temp_propagate
        # Also reset structlog config as _handle_globally_disabled_setup configures it
        structlog.reset_defaults()


    def test_scenario_1_no_initial_handlers(self, capsys: CaptureFixture[str]) -> None:
        """
        _handle_globally_disabled_setup adds a new stderr handler if temp_logger has no handlers.
        """
        from pyvider.telemetry.core import _handle_globally_disabled_setup

        assert len(self.temp_logger.handlers) == 0 # Pre-condition: no handlers

        _handle_globally_disabled_setup()

        assert len(self.temp_logger.handlers) == 1
        handler = self.temp_logger.handlers[0]
        assert isinstance(handler, stdlib_logging.StreamHandler)
        assert handler.stream == sys.stderr

        captured = capsys.readouterr()
        assert "Pyvider telemetry globally disabled." in captured.err
        assert f"[Pyvider Setup] INFO ({self.temp_logger_name}):" in captured.err


    def test_scenario_2_existing_non_stderr_handler(self, capsys: CaptureFixture[str]) -> None:
        """
        _handle_globally_disabled_setup replaces existing non-stderr handlers
        on temp_logger with a new stderr handler.
        """
        from pyvider.telemetry.core import _handle_globally_disabled_setup

        dummy_stream = io.StringIO()
        dummy_handler = stdlib_logging.StreamHandler(dummy_stream)
        self.temp_logger.addHandler(dummy_handler)

        assert len(self.temp_logger.handlers) == 1 # Pre-condition
        assert self.temp_logger.handlers[0] == dummy_handler

        _handle_globally_disabled_setup()

        assert len(self.temp_logger.handlers) == 1
        new_handler = self.temp_logger.handlers[0]
        assert new_handler != dummy_handler
        assert isinstance(new_handler, stdlib_logging.StreamHandler)
        assert new_handler.stream == sys.stderr

        # The dummy_stream associated with the removed dummy_handler should not be closed by this function.
        # (Though stdlib might close it if it owned it and it was removed - check StreamHandler docs)
        # For io.StringIO, it's not auto-closed by handler removal.
        assert not dummy_stream.closed
        dummy_stream.close() # Clean up stream

        captured = capsys.readouterr()
        assert "Pyvider telemetry globally disabled." in captured.err

    def test_scenario_3_needs_configuration_is_false(self, capsys: CaptureFixture[str]) -> None:
        """
        _handle_globally_disabled_setup does not reconfigure handlers if a suitable
        stderr handler already exists on temp_logger.
        """
        from pyvider.telemetry.core import _handle_globally_disabled_setup

        # Manually add a correctly configured stderr handler
        # The formatter must match exactly for needs_configuration to be false.
        # _config_warning_formatter is not directly importable without underscore.
        # So, we rely on the fact that if a stderr handler exists, it's considered okay.
        # The actual code: `not any(isinstance(h, stdlib_logging.StreamHandler) and h.stream == sys.stderr ...)`
        # This means any stderr handler will make `needs_configuration` false for this part.

        existing_stderr_handler = stdlib_logging.StreamHandler(sys.stderr)
        # To ensure the formatter is also considered correct by the internal logic,
        # we'd ideally use the same formatter instance or an equivalent one.
        # For this test, let's assume any stderr handler is enough to skip reconfig.
        # The function _handle_globally_disabled_setup actually checks:
        # `not temp_logger.handlers or not any(isinstance(h, stdlib_logging.StreamHandler) and h.stream == sys.stderr ...)`
        # So if temp_logger.handlers is not empty AND there is a stderr handler, it won't reconfigure.

        self.temp_logger.addHandler(existing_stderr_handler)
        self.temp_logger.setLevel(stdlib_logging.INFO) # Ensure it can log

        # Mock removeHandler to check if it's called (it shouldn't be)
        remove_handler_mock = MagicMock()
        original_remove_handler = self.temp_logger.removeHandler
        self.temp_logger.removeHandler = remove_handler_mock

        try:
            _handle_globally_disabled_setup()
        finally:
            self.temp_logger.removeHandler = original_remove_handler # Restore

        remove_handler_mock.assert_not_called() # Handlers should not have been cleared/reconfigured
        assert len(self.temp_logger.handlers) == 1 # Still has the one we added
        assert self.temp_logger.handlers[0] == existing_stderr_handler

        captured = capsys.readouterr()
        assert "Pyvider telemetry globally disabled." in captured.err
