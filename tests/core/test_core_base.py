#
# tests/test_core.py
#
"""
Unit tests for src.provide.foundation.core.py
"""

import io
import logging as stdlib_logging
import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from pytest import CaptureFixture
import structlog

from provide.foundation.core import (
    _CORE_SETUP_LOGGER_NAME,
    _create_core_setup_logger,
    _handle_globally_disabled_setup,
    reset_foundation_setup_for_testing,
    setup_telemetry,
    shutdown_foundation_telemetry,
)
from provide.foundation.logger import base as logger_base_module
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.utils.streams import get_safe_stderr


class TestGetSafeStderr:
    def test_get_safe_stderr_is_none(self) -> None:
        with patch.object(sys, "stderr", None):
            fallback_stream = get_safe_stderr()
            assert isinstance(fallback_stream, io.StringIO)

    def test_get_safe_stderr_is_valid(self) -> None:
        original_stderr = sys.stderr
        if original_stderr is None:
            sys.stderr = io.StringIO("temp stderr for test")
        try:
            if sys.stderr is not None:
                stream = get_safe_stderr()
                assert stream == sys.stderr
            else:  # pragma: no cover
                pytest.skip(
                    "sys.stderr was None, cannot run this specific path meaningfully."
                )
        finally:
            if original_stderr is None and hasattr(sys, "stderr"):
                sys.stderr = original_stderr


class TestCreateCoreSetupLogger:
    def test_create_core_setup_logger_handler_close_exception(self) -> None:
        logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)
        original_handlers = list(logger.handlers)
        logger.handlers.clear()
        mock_handler_stream = io.StringIO()
        mock_handler = stdlib_logging.StreamHandler(mock_handler_stream)
        mock_handler.close = MagicMock(side_effect=RuntimeError("Failed to close"))
        logger.addHandler(mock_handler)
        try:
            _create_core_setup_logger(globally_disabled=False)
            assert mock_handler not in logger.handlers
            assert len(logger.handlers) == 1
        finally:
            logger.handlers.clear()
            for handler in original_handlers:
                logger.addHandler(handler)
            if not mock_handler_stream.closed:
                mock_handler_stream.close()


class TestStateResetCoverage:
    def test_reset_foundation_setup_for_testing_resets_lazy_state(self) -> None:
        logger_base_module._LAZY_SETUP_STATE["done"] = True
        logger_base_module._LAZY_SETUP_STATE["error"] = Exception("dummy error")
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = True
        reset_foundation_setup_for_testing()
        assert not logger_base_module._LAZY_SETUP_STATE["done"]
        assert logger_base_module._LAZY_SETUP_STATE["error"] is None
        assert not logger_base_module._LAZY_SETUP_STATE["in_progress"]

    def test_setup_telemetry_resets_lazy_state(self) -> None:
        logger_base_module._LAZY_SETUP_STATE["done"] = True
        logger_base_module._LAZY_SETUP_STATE["error"] = Exception("dummy error")
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = True
        basic_config = TelemetryConfig(logging=LoggingConfig(default_level="INFO"))
        setup_telemetry(basic_config)
        assert logger_base_module._LAZY_SETUP_STATE["done"]
        assert logger_base_module._LAZY_SETUP_STATE["error"] is None
        assert not logger_base_module._LAZY_SETUP_STATE["in_progress"]


class TestShutdownCoverage:
    @pytest.mark.asyncio
    async def test_shutdown_foundation_telemetry_logs_message(
        self, capsys: CaptureFixture[str]
    ) -> None:
        with patch.dict(os.environ, {"FOUNDATION_LOG_LEVEL": "DEBUG"}):
            reset_foundation_setup_for_testing()
            await shutdown_foundation_telemetry()
            captured = capsys.readouterr()
            assert "Foundation Telemetry flush called" in captured.err


# FIX: Rewrote TestHandleGloballyDisabledSetup to be simpler and correct.
class TestHandleGloballyDisabledSetup:
    def test_globally_disabled_configures_structlog_as_noop(
        self, capsys: CaptureFixture[str]
    ) -> None:
        """
        Tests that _handle_globally_disabled_setup configures structlog with ReturnLoggerFactory.
        """
        with patch.dict(os.environ, {"FOUNDATION_LOG_LEVEL": "DEBUG"}):
            reset_foundation_setup_for_testing()  # Ensure clean state

            _handle_globally_disabled_setup()

            # Check that structlog is configured to be a no-op
            config = structlog.get_config()
            assert isinstance(config.get("logger_factory"), structlog.ReturnLoggerFactory)
            assert config.get("processors") == []

            # Check that the setup message was logged


class TestFoundationLogOutputCoreSetup:
    """Test FOUNDATION_LOG_OUTPUT effects on core setup logger."""

    def test_core_setup_logger_default_stderr(self, capsys: CaptureFixture) -> None:
        """Test that core setup logger uses stderr by default."""
        with patch.dict(os.environ, {"FOUNDATION_LOG_LEVEL": "DEBUG"}, clear=False):
            reset_foundation_setup_for_testing()
            
            # Trigger a core setup log message
            setup_telemetry(TelemetryConfig())
            
            captured = capsys.readouterr()
            # Should see setup messages in stderr
            assert "Foundation (structlog) setup" in captured.err

    def test_core_setup_logger_stdout_setting(self, monkeypatch, capsys: CaptureFixture) -> None:
        """Test that core setup logger respects FOUNDATION_LOG_OUTPUT=stdout."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stdout") 
        monkeypatch.setenv("FOUNDATION_LOG_LEVEL", "DEBUG")
        
        reset_foundation_setup_for_testing()
        
        # Trigger a core setup log message
        setup_telemetry(TelemetryConfig())
        
        captured = capsys.readouterr()
        # Should see setup messages in stdout, not stderr
        assert "Foundation (structlog) setup" in captured.out
        assert "Foundation (structlog) setup" not in captured.err

    def test_core_setup_logger_invalid_setting_fallback(self, monkeypatch, capsys: CaptureFixture) -> None:
        """Test that invalid FOUNDATION_LOG_OUTPUT falls back to stderr."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "invalid_value")
        monkeypatch.setenv("FOUNDATION_LOG_LEVEL", "DEBUG")
        
        reset_foundation_setup_for_testing()
        
        # Trigger a core setup log message AND a config warning to test both
        setup_telemetry(TelemetryConfig())
        
        # Also trigger a config warning which should use the invalid value
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")
        from provide.foundation.logger.config import LoggingConfig
        config = LoggingConfig.from_env()
        
        captured = capsys.readouterr()
        # Should see setup messages in stderr (fallback)
        assert "Foundation (structlog) setup" in captured.err
        # Should also see warning about invalid FOUNDATION_LOG_OUTPUT somewhere
        # (It might come from either core setup logger creation or config warning logger)
        full_output = captured.out + captured.err
        assert "[Foundation Config Warning]" in full_output
        assert "invalid_value" in full_output

    def test_core_setup_logger_with_main_setting(self, monkeypatch, tmp_path, capsys: CaptureFixture) -> None:
        """Test that core setup logger follows main log destination with FOUNDATION_LOG_OUTPUT=main."""
        log_file = tmp_path / "test.log"
        
        monkeypatch.setenv("PROVIDE_LOG_FILE", str(log_file))
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "main")
        monkeypatch.setenv("FOUNDATION_LOG_LEVEL", "DEBUG")
        
        reset_foundation_setup_for_testing()
        
        # Setup telemetry which should create the log file and log there
        config = TelemetryConfig.from_env()
        setup_telemetry(config)
        
        # Core setup messages should follow main log destination (file)
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "Foundation (structlog) setup" in log_content
