"""Tests to achieve 100% coverage."""

import sys
from unittest.mock import MagicMock, patch

import structlog

from provide.foundation.logger.base import FoundationLogger
from provide.foundation.logger.core import _LAZY_SETUP_STATE
from provide.foundation.setup import (
    reset_foundation_setup_for_testing,
)


def test_ensure_stderr_default() -> None:
    """Test that ensure_stderr_default switches from stdout to stderr."""
    from provide.foundation import streams
    from provide.foundation.streams import ensure_stderr_default

    # Reset stream state first
    from provide.foundation.streams.file import reset_streams
    reset_streams()

    # Set stream to stdout first
    streams.core._PROVIDE_LOG_STREAM = sys.stdout

    # Call the function - should switch to stderr
    ensure_stderr_default()

    # Verify it switched - use a more robust check that works in testing contexts
    # The stream should no longer be stdout and should be some form of stderr
    assert streams.core._PROVIDE_LOG_STREAM is not sys.stdout
    # In testing contexts, stderr might be wrapped, so check the name attribute
    assert hasattr(streams.core._PROVIDE_LOG_STREAM, "name")
    # The underlying stream should be stderr-like (file descriptor 2 or wrapped stderr)
    stream = streams.core._PROVIDE_LOG_STREAM
    if hasattr(stream, "fileno"):
        # In normal contexts, stderr has fileno 2
        try:
            assert stream.fileno() == 2 or stream is sys.stderr
        except (OSError, ValueError):
            # In some testing contexts, fileno() might not work, so fallback to other checks
            assert (
                stream is sys.stderr
                or "stderr" in str(stream)
                or "2" in getattr(stream, "name", "")
            )
    else:
        # If no fileno method, check if it's sys.stderr or has stderr-like characteristics
        assert stream is sys.stderr or "stderr" in str(stream)

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
    from provide.foundation.logger import core

    reset_foundation_setup_for_testing()

    logger = FoundationLogger()

    # Clear initial state
    _LAZY_SETUP_STATE["done"] = False
    _LAZY_SETUP_STATE["error"] = None
    _LAZY_SETUP_STATE["in_progress"] = False

    def set_error() -> MagicMock:
        _LAZY_SETUP_STATE["error"] = Exception("Error from other thread")
        return MagicMock()

    # Use patch to modify the lock behavior
    with patch.object(core, "_LAZY_SETUP_LOCK") as mock_lock:
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
