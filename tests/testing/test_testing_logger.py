"""Tests for logger testing utilities."""

import structlog

from provide.foundation.testing.logger import (
    reset_foundation_state,
    reset_foundation_setup_for_testing,
)
from provide.foundation.logger.core import (
    logger as foundation_logger,
    _LAZY_SETUP_STATE,
)


class TestLoggerTestingUtilities:
    """Test logger testing helper functions."""

    def test_reset_foundation_state_resets_structlog(self):
        """Test that reset_foundation_state resets structlog."""
        # Configure structlog with custom processors
        original_processors = [structlog.processors.add_log_level]
        structlog.configure(
            processors=original_processors,
            logger_factory=structlog.ReturnLoggerFactory(),
        )

        # Verify we have our custom config
        assert structlog.get_config()["processors"] == original_processors

        reset_foundation_state()

        # Should be reset to structlog defaults (not empty)
        default_config = structlog.get_config()
        assert len(default_config["processors"]) > 0  # Should have default processors
        assert (
            default_config["processors"] != original_processors
        )  # Should be different from our custom config

    def test_reset_foundation_state_resets_logger_state(self):
        """Test that foundation logger state is reset."""
        # Set some state on the logger
        foundation_logger._is_configured_by_setup = True
        foundation_logger._active_config = "test_config"
        foundation_logger._active_resolved_emoji_config = "test_emoji"

        reset_foundation_state()

        # Should be reset
        assert foundation_logger._is_configured_by_setup is False
        assert foundation_logger._active_config is None
        assert foundation_logger._active_resolved_emoji_config is None

    def test_reset_foundation_state_resets_lazy_setup_state(self):
        """Test that lazy setup state is reset."""
        # Modify lazy setup state
        _LAZY_SETUP_STATE.update(
            {"done": True, "error": "test_error", "in_progress": True}
        )

        reset_foundation_state()

        # Should be reset to defaults
        assert _LAZY_SETUP_STATE["done"] is False
        assert _LAZY_SETUP_STATE["error"] is None
        assert _LAZY_SETUP_STATE["in_progress"] is False

    def test_reset_foundation_setup_for_testing_calls_reset_state(self):
        """Test that public function calls internal reset."""
        # Set some state
        foundation_logger._is_configured_by_setup = True
        _LAZY_SETUP_STATE["done"] = True

        reset_foundation_setup_for_testing()

        # Should be reset
        assert foundation_logger._is_configured_by_setup is False
        assert _LAZY_SETUP_STATE["done"] is False

    def test_reset_functions_are_idempotent(self):
        """Test that reset functions can be called multiple times safely."""
        # Should not raise any exceptions
        reset_foundation_state()
        reset_foundation_state()
        reset_foundation_setup_for_testing()
        reset_foundation_setup_for_testing()

        # State should remain consistent
        assert foundation_logger._is_configured_by_setup is False
        assert _LAZY_SETUP_STATE["done"] is False

    def test_reset_preserves_logger_functionality(self):
        """Test that logger still works after reset."""
        reset_foundation_setup_for_testing()

        # Logger should still be callable
        logger_instance = foundation_logger.get_logger("test")
        assert logger_instance is not None

        # Should be able to call logging methods (though they may not output anything)
        try:
            logger_instance.info("test message")
        except Exception as e:
            pytest.fail(f"Logger should work after reset, but got: {e}")

    def test_reset_state_full_cycle(self):
        """Test full cycle of setup, use, and reset."""
        # Start with clean state
        reset_foundation_setup_for_testing()

        initial_config_state = foundation_logger._is_configured_by_setup
        initial_lazy_state = _LAZY_SETUP_STATE.copy()

        # Simulate some usage that changes state
        foundation_logger._is_configured_by_setup = True
        _LAZY_SETUP_STATE["done"] = True
        _LAZY_SETUP_STATE["in_progress"] = False

        # Reset should bring back to initial state
        reset_foundation_setup_for_testing()

        assert foundation_logger._is_configured_by_setup == initial_config_state
        assert _LAZY_SETUP_STATE == initial_lazy_state
