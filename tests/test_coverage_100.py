"""Tests to achieve 100% coverage."""
import sys
from unittest.mock import patch, MagicMock
import structlog
from provide.foundation.core import _set_log_stream_for_testing, reset_foundation_setup_for_testing
from provide.foundation.logger.base import FoundationLogger, _LAZY_SETUP_STATE


def test_ensure_stderr_default():
    """Test that _ensure_stderr_default switches from stdout to stderr."""
    from provide.foundation import core
    from provide.foundation.core import _ensure_stderr_default
    
    # Set stream to stdout first
    core._FOUNDATION_LOG_STREAM = sys.stdout
    
    # Call the function - should switch to stderr
    _ensure_stderr_default()
    
    # Verify it switched
    assert core._FOUNDATION_LOG_STREAM is sys.stderr
    
    # Reset
    reset_foundation_setup_for_testing()


def test_check_structlog_already_disabled_return_factory():
    """Test the path where structlog is configured with ReturnLoggerFactory."""
    reset_foundation_setup_for_testing()
    
    logger = FoundationLogger()
    
    # Mock structlog.get_config to return a config with ReturnLoggerFactory
    mock_config = {'logger_factory': structlog.ReturnLoggerFactory()}
    
    with patch('structlog.get_config', return_value=mock_config):
        result = logger._check_structlog_already_disabled()
        
    assert result is True
    assert _LAZY_SETUP_STATE["done"] is True
    
    # Reset
    reset_foundation_setup_for_testing()


def test_ensure_configured_already_disabled():
    """Test _ensure_configured when structlog is already disabled."""
    reset_foundation_setup_for_testing()
    
    logger = FoundationLogger()
    
    # Mock the check to return True
    with patch.object(logger, '_check_structlog_already_disabled', return_value=True):
        logger._ensure_configured()
        # Should return early without doing setup
    
    # Reset
    reset_foundation_setup_for_testing()


def test_logger_base_error_paths():
    """Test error handling paths in logger base."""
    reset_foundation_setup_for_testing()
    
    logger = FoundationLogger()
    
    # Set up state to trigger the error path where setup failed
    _LAZY_SETUP_STATE["error"] = Exception("Test error")
    _LAZY_SETUP_STATE["done"] = False
    
    # Mock emergency fallback
    with patch.object(logger, '_setup_emergency_fallback') as mock_fallback:
        logger._ensure_configured()
        mock_fallback.assert_called_once()
    
    # Reset
    reset_foundation_setup_for_testing()