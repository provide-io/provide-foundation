"""Tests for Hub initialization with process title support."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest
from pytest import MonkeyPatch

from provide.foundation.config.foundation import FoundationConfig
from provide.foundation.hub.initialization import InitializationCoordinator
from provide.foundation.hub.registry import Registry
from provide.foundation.logger.config.telemetry import TelemetryConfig


class TestProcessTitleInitialization(FoundationTestCase):
    """Test process title configuration during initialization."""

    def test_initialize_with_foundation_config_and_process_title(self) -> None:
        """Test initialization with FoundationConfig containing process_title."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        config = FoundationConfig(
            telemetry=TelemetryConfig(service_name="test-service"),
            process_title="test-app",
        )

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            coordinator.initialize_foundation(registry, config)

            # Verify process title was set
            mock_set_title.assert_called_once_with("test-app")

    def test_initialize_with_foundation_config_no_process_title(self) -> None:
        """Test initialization with FoundationConfig without process_title."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        config = FoundationConfig(
            telemetry=TelemetryConfig(service_name="test-service"),
            process_title=None,
        )

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            coordinator.initialize_foundation(registry, config)

            # Verify process title was NOT set (None value)
            mock_set_title.assert_not_called()

    def test_initialize_with_telemetry_config_auto_wraps(self) -> None:
        """Test initialization with TelemetryConfig auto-wraps to FoundationConfig."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        # Pass TelemetryConfig directly (backward compatibility)
        telemetry_config = TelemetryConfig(service_name="test-service")

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            actual_config, _ = coordinator.initialize_foundation(registry, telemetry_config)

            # Verify it was wrapped in FoundationConfig
            assert isinstance(actual_config, FoundationConfig)
            assert actual_config.telemetry == telemetry_config
            assert actual_config.process_title is None

            # Process title should not be set
            mock_set_title.assert_not_called()

    def test_initialize_from_env_with_process_title(self, monkeypatch: MonkeyPatch) -> None:
        """Test initialization from environment with PROVIDE_PROCESS_TITLE."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "env-app")
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "env-service")

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            config, _ = coordinator.initialize_foundation(registry, None)

            # Verify config loaded from environment
            assert isinstance(config, FoundationConfig)
            assert config.process_title == "env-app"
            assert config.telemetry.service_name == "env-service"

            # Verify process title was set
            mock_set_title.assert_called_once_with("env-app")

    def test_setup_process_title_exception_suppressed(self) -> None:
        """Test that exceptions in _setup_process_title are suppressed."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        config = FoundationConfig(
            telemetry=TelemetryConfig(),
            process_title="test-app",
        )

        # Mock set_process_title to raise an exception
        with patch(
            "provide.foundation.process.title.set_process_title",
            side_effect=RuntimeError("Failed to set title"),
        ):
            # Should not raise - exception should be suppressed
            actual_config, _ = coordinator.initialize_foundation(registry, config)

            # Initialization should complete successfully
            assert coordinator.is_initialized()
            assert actual_config == config

    def test_setup_process_title_import_error_suppressed(self) -> None:
        """Test that import errors in _setup_process_title are suppressed."""
        coordinator = InitializationCoordinator()

        config = FoundationConfig(
            telemetry=TelemetryConfig(),
            process_title="test-app",
        )

        # This should not raise even if imports fail
        coordinator._setup_process_title(config)

    def test_setup_process_title_with_non_foundation_config(self) -> None:
        """Test _setup_process_title with TelemetryConfig (not FoundationConfig)."""
        coordinator = InitializationCoordinator()

        telemetry_config = TelemetryConfig(service_name="test")

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            # Passing TelemetryConfig directly should not set process title
            coordinator._setup_process_title(telemetry_config)

            mock_set_title.assert_not_called()


class TestInitializationConfigExtraction(FoundationTestCase):
    """Test config extraction for logger initialization."""

    def test_logger_initialization_extracts_telemetry_config(self) -> None:
        """Test that _initialize_logger extracts telemetry from FoundationConfig."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        telemetry = TelemetryConfig(service_name="extract-test")
        config = FoundationConfig(
            telemetry=telemetry,
            process_title="test-app",
        )

        with patch("provide.foundation.logger.core.FoundationLogger") as mock_logger_class:
            mock_logger = mock_logger_class.return_value

            coordinator._initialize_logger(config, registry)

            # Verify logger.setup was called with TelemetryConfig, not FoundationConfig
            mock_logger.setup.assert_called_once_with(telemetry)

    def test_logger_initialization_with_telemetry_config_directly(self) -> None:
        """Test _initialize_logger with TelemetryConfig directly."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        telemetry = TelemetryConfig(service_name="direct-test")

        with patch("provide.foundation.logger.core.FoundationLogger") as mock_logger_class:
            mock_logger = mock_logger_class.return_value

            coordinator._initialize_logger(telemetry, registry)

            # Should pass TelemetryConfig directly to setup
            mock_logger.setup.assert_called_once_with(telemetry)


class TestFoundationConfigFallback(FoundationTestCase):
    """Test FoundationConfig fallback behavior."""

    def test_initialize_config_fallback_creates_foundation_config(self) -> None:
        """Test that fallback creates FoundationConfig, not TelemetryConfig."""
        coordinator = InitializationCoordinator()

        # Mock FoundationConfig.from_env to raise a non-import error
        with patch(
            "provide.foundation.config.foundation.FoundationConfig.from_env",
            side_effect=ValueError("Parse error"),
        ):
            config = coordinator._initialize_config(None)

            # Should fallback to minimal FoundationConfig
            assert isinstance(config, FoundationConfig)
            assert isinstance(config.telemetry, TelemetryConfig)
            assert config.process_title is None

    def test_initialize_config_import_error_raises(self) -> None:
        """Test that import errors are not suppressed."""
        coordinator = InitializationCoordinator()

        with (
            patch(
                "provide.foundation.config.foundation.FoundationConfig.from_env",
                side_effect=ImportError("Cannot import"),
            ),
            pytest.raises(ImportError, match="Cannot import"),
        ):
            coordinator._initialize_config(None)


class TestProcessTitleIntegration(FoundationTestCase):
    """Integration tests for process title with full initialization."""

    def test_full_initialization_flow_with_process_title(self, monkeypatch: MonkeyPatch) -> None:
        """Test complete initialization flow with process title."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "integration-app")
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "integration-service")
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "DEBUG")

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            config, logger = coordinator.initialize_foundation(registry)

            # Verify config
            assert isinstance(config, FoundationConfig)
            assert config.process_title == "integration-app"
            assert config.telemetry.service_name == "integration-service"
            assert config.telemetry.logging.log_level == "DEBUG"

            # Verify process title was set
            mock_set_title.assert_called_once_with("integration-app")

            # Verify initialization completed
            assert coordinator.is_initialized()
            assert logger is not None

    def test_force_reinitialization_with_new_process_title(self) -> None:
        """Test force re-initialization with different process title."""
        coordinator = InitializationCoordinator()
        registry = Registry()

        # First initialization
        config1 = FoundationConfig(
            telemetry=TelemetryConfig(service_name="service1"),
            process_title="app1",
        )

        with patch("provide.foundation.process.title.set_process_title") as mock_set_title:
            coordinator.initialize_foundation(registry, config1)
            assert mock_set_title.call_count == 1
            mock_set_title.assert_called_with("app1")

            # Force re-initialization with new config
            config2 = FoundationConfig(
                telemetry=TelemetryConfig(service_name="service2"),
                process_title="app2",
            )
            coordinator.initialize_foundation(registry, config2, force=True)

            # Process title should be set again with new value
            assert mock_set_title.call_count == 2
            assert mock_set_title.call_args[0][0] == "app2"


# <3 🧱🤝🌐🪄
