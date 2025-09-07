"""Test coverage for logger setup __init__ module."""


class TestLoggerSetupInitCoverage:
    """Test logger setup __init__ module functionality."""
    
    def test_internal_setup_import(self):
        """Test internal_setup can be imported."""
        from provide.foundation.logger.setup import internal_setup
        assert internal_setup is not None
        assert callable(internal_setup)
    
    def test_conditional_import_success(self):
        """Test conditional import with successful testing import."""
        from provide.foundation.logger.setup import _has_testing, reset_for_testing
        
        # In the current environment, testing should be available
        assert _has_testing is True
        assert reset_for_testing is not None
        assert callable(reset_for_testing)
    
    def test_coordinator_import_available(self):
        """Test that internal_setup comes from coordinator module."""
        from provide.foundation.logger.setup.coordinator import internal_setup as coord_setup
        from provide.foundation.logger.setup import internal_setup
        
        # Should be the same function
        assert internal_setup == coord_setup
    
    def test_all_exports_basic(self):
        """Test __all__ contains expected basic exports."""
        from provide.foundation.logger.setup import __all__
        
        assert "internal_setup" in __all__
        # reset_for_testing should be included since testing is available
        assert "reset_for_testing" in __all__
    
    def test_has_testing_flag(self):
        """Test _has_testing flag is properly set."""
        from provide.foundation.logger.setup import _has_testing
        
        # Should be True in current environment since testing module exists
        assert _has_testing is True
    
