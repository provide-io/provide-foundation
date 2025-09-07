"""Test coverage for logger config module re-exports."""

import provide.foundation.logger.config as logger_config_module


class TestLoggerConfigModuleCoverage:
    """Test logger config module re-exports."""
    
    def test_logging_config_import(self):
        """Test LoggingConfig can be imported from config module."""
        LoggingConfig = logger_config_module.LoggingConfig
        assert LoggingConfig is not None
        assert hasattr(LoggingConfig, '__name__')
    
    def test_telemetry_config_import(self):
        """Test TelemetryConfig can be imported from config module."""
        TelemetryConfig = logger_config_module.TelemetryConfig
        assert TelemetryConfig is not None
        assert hasattr(TelemetryConfig, '__name__')
    
    def test_all_exports(self):
        """Test __all__ contains expected exports."""
        expected = ["LoggingConfig", "TelemetryConfig"]
        assert logger_config_module.__all__ == expected
    
    def test_module_imports_work(self):
        """Test that module-level imports execute correctly."""
        # This forces the module to be fully loaded and imports to be executed
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
        
        assert LoggingConfig is not None
        assert TelemetryConfig is not None
        assert hasattr(LoggingConfig, '__module__')
        assert hasattr(TelemetryConfig, '__module__')