#
# test_config_imports.py
#
"""
Tests for logger/config.py module imports.
"""

import pytest


class TestConfigImports:
    def test_imports_logging_config(self):
        """Test that LoggingConfig can be imported from config module."""
        from provide.foundation.logger.config import LoggingConfig
        
        assert LoggingConfig is not None
        assert hasattr(LoggingConfig, '__name__')
    
    def test_imports_telemetry_config(self):
        """Test that TelemetryConfig can be imported from config module."""
        from provide.foundation.logger.config import TelemetryConfig
        
        assert TelemetryConfig is not None
        assert hasattr(TelemetryConfig, '__name__')
    
    def test_module_all_exports(self):
        """Test that __all__ contains expected exports."""
        from provide.foundation.logger import config
        
        assert hasattr(config, '__all__')
        assert 'LoggingConfig' in config.__all__
        assert 'TelemetryConfig' in config.__all__
    
    def test_direct_module_import(self):
        """Test importing the config module directly."""
        from provide.foundation.logger import config as config_module
        
        assert hasattr(config_module, 'LoggingConfig')
        assert hasattr(config_module, 'TelemetryConfig')
        assert hasattr(config_module, '__all__')