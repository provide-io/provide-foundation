"""Test coverage for logger config module re-exports."""

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig


class TestLoggerConfigModuleCoverage:
    """Test logger config module re-exports."""
    
    def test_logging_config_import(self):
        """Test LoggingConfig can be imported from config module."""
        assert LoggingConfig is not None
        assert hasattr(LoggingConfig, '__name__')
    
    def test_telemetry_config_import(self):
        """Test TelemetryConfig can be imported from config module."""
        assert TelemetryConfig is not None
        assert hasattr(TelemetryConfig, '__name__')
    
    def test_all_exports(self):
        """Test __all__ contains expected exports."""
        from provide.foundation.logger.config import __all__
        
        expected = ["LoggingConfig", "TelemetryConfig"]
        assert __all__ == expected