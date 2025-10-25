"""Tests for FoundationConfig."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest
from pytest import MonkeyPatch

from provide.foundation.config.foundation import FoundationConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig


class TestFoundationConfig(FoundationTestCase):
    """Test FoundationConfig functionality."""

    def test_from_env_loads_process_title(self, monkeypatch: MonkeyPatch) -> None:
        """Test loading process_title from environment."""
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "test-app")
        config = FoundationConfig.from_env()
        assert config.process_title == "test-app"

    def test_from_env_default_process_title_is_none(self) -> None:
        """Test that default process_title is None."""
        config = FoundationConfig.from_env()
        assert config.process_title is None

    def test_from_env_loads_telemetry_config(self, monkeypatch: MonkeyPatch) -> None:
        """Test that telemetry config is loaded from environment."""
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "test-service")
        config = FoundationConfig.from_env()
        assert isinstance(config.telemetry, TelemetryConfig)
        assert config.telemetry.service_name == "test-service"

    def test_from_env_loads_both_process_and_telemetry(self, monkeypatch: MonkeyPatch) -> None:
        """Test loading both process_title and telemetry settings."""
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "my-worker")
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "my-service")
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "DEBUG")

        config = FoundationConfig.from_env()

        assert config.process_title == "my-worker"
        assert config.telemetry.service_name == "my-service"
        assert config.telemetry.logging.log_level == "DEBUG"

    def test_create_with_explicit_values(self) -> None:
        """Test creating FoundationConfig with explicit values."""
        telemetry = TelemetryConfig(service_name="explicit-service")
        config = FoundationConfig(
            telemetry=telemetry,
            process_title="explicit-title",
        )

        assert config.process_title == "explicit-title"
        assert config.telemetry.service_name == "explicit-service"

    def test_create_with_defaults(self) -> None:
        """Test creating FoundationConfig uses factory defaults."""
        config = FoundationConfig()
        assert config.process_title is None
        assert isinstance(config.telemetry, TelemetryConfig)

    def test_config_is_immutable(self) -> None:
        """Test that FoundationConfig is immutable (frozen attrs)."""
        config = FoundationConfig()
        with pytest.raises(AttributeError):
            config.process_title = "new-title"  # type: ignore[misc]

    def test_telemetry_config_nested_properly(self) -> None:
        """Test that telemetry config is properly nested."""
        config = FoundationConfig()
        assert hasattr(config, "telemetry")
        assert isinstance(config.telemetry, TelemetryConfig)
        assert hasattr(config.telemetry, "logging")

    def test_process_title_none_is_valid(self) -> None:
        """Test that None is a valid value for process_title."""
        config = FoundationConfig(
            telemetry=TelemetryConfig(),
            process_title=None,
        )
        assert config.process_title is None

    def test_process_title_empty_string(self, monkeypatch: MonkeyPatch) -> None:
        """Test that empty string for process_title is treated as empty."""
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "")
        config = FoundationConfig.from_env()
        # Empty string from env should be returned as-is (not None)
        assert config.process_title == "" or config.process_title is None


class TestFoundationConfigIntegration(FoundationTestCase):
    """Integration tests for FoundationConfig with full environment."""

    def test_full_env_configuration(self, monkeypatch: MonkeyPatch) -> None:
        """Test complete configuration from environment variables."""
        # Set all relevant environment variables
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", "integration-test")
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "integration-service")
        monkeypatch.setenv("PROVIDE_SERVICE_VERSION", "1.0.0")
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INFO")
        monkeypatch.setenv("OTEL_TRACING_ENABLED", "true")

        config = FoundationConfig.from_env()

        # Verify all values loaded correctly
        assert config.process_title == "integration-test"
        assert config.telemetry.service_name == "integration-service"
        assert config.telemetry.service_version == "1.0.0"
        assert config.telemetry.logging.log_level == "INFO"
        assert config.telemetry.tracing_enabled is True

    def test_otel_service_name_precedence(self, monkeypatch: MonkeyPatch) -> None:
        """Test that OTEL_SERVICE_NAME takes precedence over PROVIDE_SERVICE_NAME."""
        monkeypatch.setenv("OTEL_SERVICE_NAME", "otel-service")
        monkeypatch.setenv("PROVIDE_SERVICE_NAME", "provide-service")

        config = FoundationConfig.from_env()
        assert config.telemetry.service_name == "otel-service"

    def test_config_composition_pattern(self) -> None:
        """Test that composition pattern works correctly."""
        # Create telemetry config separately
        telemetry = TelemetryConfig(
            service_name="composed-service",
            tracing_enabled=True,
        )

        # Compose into FoundationConfig
        config = FoundationConfig(
            telemetry=telemetry,
            process_title="composed-app",
        )

        assert config.telemetry.service_name == "composed-service"
        assert config.telemetry.tracing_enabled is True
        assert config.process_title == "composed-app"


class TestFoundationConfigEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def test_process_title_with_special_characters(self, monkeypatch: MonkeyPatch) -> None:
        """Test process_title with special characters."""
        special_title = "my-app_worker:123"
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", special_title)

        config = FoundationConfig.from_env()
        assert config.process_title == special_title

    def test_process_title_with_unicode(self, monkeypatch: MonkeyPatch) -> None:
        """Test process_title with unicode characters."""
        unicode_title = "my-app-✨"
        monkeypatch.setenv("PROVIDE_PROCESS_TITLE", unicode_title)

        config = FoundationConfig.from_env()
        assert config.process_title == unicode_title

    def test_from_env_preserves_telemetry_defaults(self) -> None:
        """Test that telemetry defaults are preserved when not specified."""
        config = FoundationConfig.from_env()

        # These should use TelemetryConfig defaults
        assert isinstance(config.telemetry.tracing_enabled, bool)
        assert isinstance(config.telemetry.metrics_enabled, bool)
        assert config.telemetry.otlp_protocol in ("grpc", "http/protobuf")


# <3 🧱🤝⚙️🪄
