"""Test coverage for logger setup __init__ module."""

from unittest.mock import patch, Mock
import pytest


class TestLoggerSetupInitCoverage:
    """Test logger setup __init__ module functionality."""
    
    def test_internal_setup_import(self):
        """Test internal_setup can be imported."""
        from provide.foundation.logger.setup import internal_setup
        assert internal_setup is not None
        assert callable(internal_setup)
    
    def test_all_exports_without_testing(self):
        """Test __all__ contains expected exports without testing utilities."""
        # Mock the testing import to fail
        with patch('builtins.__import__', side_effect=ImportError):
            # Need to reload the module to test the ImportError path
            import importlib
            import sys
            
            # Remove if already loaded
            if 'provide.foundation.logger.setup' in sys.modules:
                del sys.modules['provide.foundation.logger.setup']
            
            # Import with mocked failure
            import provide.foundation.logger.setup as setup_module
            
            assert "internal_setup" in setup_module.__all__
            assert "reset_for_testing" not in setup_module.__all__
            assert setup_module._has_testing is False
            assert setup_module.reset_for_testing is None
    
    def test_all_exports_with_testing(self):
        """Test __all__ contains expected exports with testing utilities."""
        # Mock successful import
        mock_reset = Mock()
        
        with patch('builtins.__import__') as mock_import:
            def side_effect(name, *args, **kwargs):
                if name == 'provide.foundation.logger.setup.testing':
                    mock_module = Mock()
                    mock_module.reset_foundation_setup_for_testing = mock_reset
                    return mock_module
                # Fall back to real imports for other modules
                return __import__(name, *args, **kwargs)
            
            mock_import.side_effect = side_effect
            
            # Need to reload the module to test the successful import path
            import importlib
            import sys
            
            # Remove if already loaded
            if 'provide.foundation.logger.setup' in sys.modules:
                del sys.modules['provide.foundation.logger.setup']
            
            # Import with mocked success
            import provide.foundation.logger.setup as setup_module
            
            assert "internal_setup" in setup_module.__all__
            assert "reset_for_testing" in setup_module.__all__
            assert setup_module._has_testing is True
            assert setup_module.reset_for_testing == mock_reset
    
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