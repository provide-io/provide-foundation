"""Test coverage for logger setup __init__ module."""

import sys


class TestLoggerSetupInitCoverage:
    """Test logger setup __init__ module functionality."""

    def setup_method(self):
        """Clear module state before each test to ensure isolation."""
        # Clear logger setup modules from cache
        modules_to_clear = [
            "provide.foundation.logger.setup",
            "provide.foundation.logger.setup.coordinator",
        ]

        # Save modules that we might restore
        self.saved_modules = {}
        for mod in modules_to_clear:
            if mod in sys.modules:
                self.saved_modules[mod] = sys.modules[mod]
                del sys.modules[mod]

    def teardown_method(self):
        """Restore module state after test if needed."""
        # Only restore if we have saved modules and they're still not in cache
        for mod_name, module in self.saved_modules.items():
            if mod_name not in sys.modules:
                sys.modules[mod_name] = module

    def test_internal_setup_import(self):
        """Test internal_setup can be imported."""
        from provide.foundation.logger.setup import internal_setup

        assert internal_setup is not None
        assert callable(internal_setup)

    def test_conditional_import_success(self):
        """Test conditional import functionality works correctly."""
        from provide.foundation.logger.setup import _has_testing, reset_for_testing

        # Test the consistency of the conditional import logic
        if _has_testing:
            # If _has_testing is True, reset_for_testing should be available
            assert reset_for_testing is not None
            assert callable(reset_for_testing)
        else:
            # If _has_testing is False, reset_for_testing should be None
            assert reset_for_testing is None

    def test_coordinator_import_available(self):
        """Test that internal_setup comes from coordinator module."""
        from provide.foundation.logger.setup import internal_setup
        from provide.foundation.logger.setup.coordinator import (
            internal_setup as coord_setup,
        )

        # Should be the same function
        assert internal_setup == coord_setup

    def test_all_exports_basic(self):
        """Test __all__ contains expected basic exports."""
        from provide.foundation.logger.setup import __all__

        assert "internal_setup" in __all__
        # Testing utilities have been moved to testkit
        # reset_foundation_setup_for_testing is now in provide.testkit.logger
        assert "reset_for_testing" not in __all__

    def test_no_testing_flag(self):
        """Test that _has_testing flag no longer exists since testing was moved to testkit."""
        from provide.foundation.logger import setup

        # _has_testing should not exist anymore
        assert not hasattr(setup, '_has_testing')
