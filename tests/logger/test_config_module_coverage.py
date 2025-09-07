"""Test coverage for logger config module re-exports."""

from provide.foundation.logger import config
from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.logger.config.logging import LoggingConfig as DirectLoggingConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig as DirectTelemetryConfig


class TestLoggerConfigModuleCoverage:
    """Test logger config module re-exports for coverage."""

    def test_logging_config_reexport(self):
        """Test LoggingConfig is properly re-exported."""
        assert LoggingConfig is DirectLoggingConfig
        assert hasattr(config, 'LoggingConfig')
        assert config.LoggingConfig is DirectLoggingConfig

    def test_telemetry_config_reexport(self):
        """Test TelemetryConfig is properly re-exported."""
        assert TelemetryConfig is DirectTelemetryConfig
        assert hasattr(config, 'TelemetryConfig')
        assert config.TelemetryConfig is DirectTelemetryConfig

    def test_all_exports(self):
        """Test __all__ contains expected exports."""
        assert hasattr(config, '__all__')
        assert 'LoggingConfig' in config.__all__
        assert 'TelemetryConfig' in config.__all__
        assert len(config.__all__) == 2

    def test_module_imports_work(self):
        """Test module imports work correctly."""
        # Test direct imports
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
        
        # Test that they are the correct classes
        assert LoggingConfig.__name__ == 'LoggingConfig'
        assert TelemetryConfig.__name__ == 'TelemetryConfig'
        
        # Test that we can create instances (basic smoke test)
        logging_config = LoggingConfig()
        telemetry_config = TelemetryConfig()
        
        assert logging_config is not None
        assert telemetry_config is not None