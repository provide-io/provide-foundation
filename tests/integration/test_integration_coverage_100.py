"""Tests to achieve 100% coverage."""

import sys
from unittest.mock import MagicMock, patch

import structlog

from provide.foundation.core import (
    reset_foundation_setup_for_testing,
)
from provide.foundation.logger.base import _LAZY_SETUP_STATE, FoundationLogger


def test_ensure_stderr_default() -> None:
    """Test that _ensure_stderr_default switches from stdout to stderr."""
    from provide.foundation import core
    from provide.foundation.core import _ensure_stderr_default

    # Set stream to stdout first
    core._PROVIDE_LOG_STREAM = sys.stdout

    # Call the function - should switch to stderr
    _ensure_stderr_default()

    # Verify it switched
    assert core._PROVIDE_LOG_STREAM is sys.stderr

    # Reset
    reset_foundation_setup_for_testing()


def test_check_structlog_already_disabled_return_factory() -> None:
    """Test the path where structlog is configured with ReturnLoggerFactory."""
    reset_foundation_setup_for_testing()

    logger = FoundationLogger()

    # Mock structlog.get_config to return a config with ReturnLoggerFactory
    mock_config = {"logger_factory": structlog.ReturnLoggerFactory()}

    with patch("structlog.get_config", return_value=mock_config):
        result = logger._check_structlog_already_disabled()

    assert result is True
    assert _LAZY_SETUP_STATE["done"] is True

    # Reset
    reset_foundation_setup_for_testing()


def test_ensure_configured_already_disabled() -> None:
    """Test _ensure_configured when structlog is already disabled."""
    reset_foundation_setup_for_testing()

    logger = FoundationLogger()

    # Mock the check to return True
    with patch.object(logger, "_check_structlog_already_disabled", return_value=True):
        logger._ensure_configured()
        # Should return early without doing setup

    # Reset
    reset_foundation_setup_for_testing()


def test_logger_base_error_paths() -> None:
    """Test error handling paths in logger base."""
    reset_foundation_setup_for_testing()

    logger = FoundationLogger()

    # Set up state to trigger the error path where setup failed
    _LAZY_SETUP_STATE["error"] = Exception("Test error")
    _LAZY_SETUP_STATE["done"] = False

    # Mock emergency fallback
    with patch.object(logger, "_setup_emergency_fallback") as mock_fallback:
        logger._ensure_configured()
        mock_fallback.assert_called_once()

    # Reset
    reset_foundation_setup_for_testing()


def test_logger_base_error_while_waiting_for_lock() -> None:
    """Test error path when error is set while waiting for lock."""
    from provide.foundation.logger import base

    reset_foundation_setup_for_testing()

    logger = FoundationLogger()

    # Clear initial state
    _LAZY_SETUP_STATE["done"] = False
    _LAZY_SETUP_STATE["error"] = None
    _LAZY_SETUP_STATE["in_progress"] = False

    def set_error():
        _LAZY_SETUP_STATE["error"] = Exception("Error from other thread")
        return MagicMock()

    # Use patch to modify the lock behavior
    with patch.object(base, "_LAZY_SETUP_LOCK") as mock_lock:
        # Configure the lock's context manager behavior
        mock_lock.__enter__ = MagicMock(side_effect=set_error)
        mock_lock.__exit__ = MagicMock(return_value=None)

        # Mock emergency fallback to verify it's called
        with patch.object(logger, "_setup_emergency_fallback") as mock_fallback:
            logger._ensure_configured()
            # The emergency fallback should be called due to the error
            mock_fallback.assert_called()

    # Reset
    reset_foundation_setup_for_testing()
