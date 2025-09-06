"""Test coverage for logger config module imports."""

import pytest


class TestLoggerConfigImports:
    """Test logger config module import functionality."""
    
    def test_logging_config_import(self):
        """Test LoggingConfig can be imported from config module."""
        from provide.foundation.logger.config import LoggingConfig
        
        # Verify it's importable
        assert LoggingConfig is not None
        assert hasattr(LoggingConfig, '__name__')
    
    def test_telemetry_config_import(self):
        """Test TelemetryConfig can be imported from config module.""" 
        from provide.foundation.logger.config import TelemetryConfig
        
        # Verify it's importable
        assert TelemetryConfig is not None
        assert hasattr(TelemetryConfig, '__name__')
    
    def test_all_exports_available(self):
        """Test that __all__ exports are available."""
        import provide.foundation.logger.config as config
        
        # Verify __all__ is defined
        assert hasattr(config, '__all__')
        assert isinstance(config.__all__, list)
        
        # Verify all items in __all__ are importable
        for item_name in config.__all__:
            assert hasattr(config, item_name)
            item = getattr(config, item_name)
            assert item is not None
    
    def test_module_has_expected_exports(self):
        """Test module exports expected classes."""
        import provide.foundation.logger.config as config
        
        expected_exports = ['LoggingConfig', 'TelemetryConfig']
        
        for export in expected_exports:
            assert hasattr(config, export), f"Missing export: {export}"
            
        # Verify __all__ contains expected exports
        assert set(config.__all__) == set(expected_exports)