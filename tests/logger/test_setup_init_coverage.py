"""Test coverage for logger setup __init__ module."""

import sys


class TestLoggerSetupInitCoverage:
    """Test logger setup __init__ module functionality."""

    def setup_method(self):
        """Clear module state before each test to ensure isolation."""
        # Clear logger setup modules from cache
        modules_to_clear = [
            'provide.foundation.logger.setup',
            'provide.foundation.logger.setup.testing',
            'provide.foundation.logger.setup.coordinator',
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
        from provide.foundation.logger.setup.coordinator import (
            internal_setup as coord_setup,
        )
        from provide.foundation.logger.setup import internal_setup

        # Should be the same function
        assert internal_setup == coord_setup

    def test_all_exports_basic(self):
        """Test __all__ contains expected basic exports."""
        from provide.foundation.logger.setup import __all__

        assert "internal_setup" in __all__
        # reset_for_testing should be included if testing utilities are available
        try:
            from provide.foundation.logger.setup.testing import (
                reset_foundation_setup_for_testing,
            )

            # If testing module is importable, reset_for_testing should be exported
            assert "reset_for_testing" in __all__
        except ImportError:
            # If testing module is not available, that's okay for this test
            pass

    def test_has_testing_flag(self):
        """Test _has_testing flag is consistent with testing module availability."""
        from provide.foundation.logger.setup import _has_testing

        # Check if testing module is actually importable
        try:
            from provide.foundation.logger.setup.testing import (
                reset_foundation_setup_for_testing,
            )

            testing_available = True
        except ImportError:
            testing_available = False

        # _has_testing should match actual availability
        assert _has_testing == testing_available
