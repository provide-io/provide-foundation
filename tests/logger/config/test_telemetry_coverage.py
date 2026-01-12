#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for logger/config/telemetry.py.

These tests target uncovered lines and edge cases in telemetry configuration."""

from __future__ import annotations

import base64

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.logger.config.telemetry import (
    TelemetryConfig,
    _get_service_name,
    _get_service_version,
)


class TestGetServiceName(FoundationTestCase):
    """Test _get_service_name() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_returns_otel_service_name_when_set(self) -> None:
        """Test OTEL_SERVICE_NAME is returned when set."""
        with patch.dict("os.environ", {"OTEL_SERVICE_NAME": "otel-service"}):
            assert _get_service_name() == "otel-service"

    def test_returns_provide_service_name_when_otel_not_set(self) -> None:
        """Test PROVIDE_SERVICE_NAME is returned when OTEL_SERVICE_NAME not set."""
        with patch.dict("os.environ", {"PROVIDE_SERVICE_NAME": "provide-service"}, clear=True):
            assert _get_service_name() == "provide-service"

    def test_otel_service_name_takes_precedence(self) -> None:
        """Test OTEL_SERVICE_NAME takes precedence over PROVIDE_SERVICE_NAME."""
        with patch.dict(
            "os.environ",
            {
                "OTEL_SERVICE_NAME": "otel-service",
                "PROVIDE_SERVICE_NAME": "provide-service",
            },
        ):
            assert _get_service_name() == "otel-service"

    def test_returns_none_when_neither_set(self) -> None:
        """Test returns None when neither environment variable is set."""
        with patch.dict("os.environ", {}, clear=True):
            assert _get_service_name() is None


class TestGetServiceVersion(FoundationTestCase):
    """Test _get_service_version() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_returns_version_when_available(self) -> None:
        """Test returns version when get_version succeeds."""
        mock_get_version = Mock(return_value="1.2.3")

        with patch("provide.foundation.utils.versioning.get_version", mock_get_version):
            version = _get_service_version()

            assert version == "1.2.3"
            mock_get_version.assert_called_once_with("provide-foundation")

    def test_returns_none_on_import_error(self) -> None:
        """Test returns None when versioning module cannot be imported."""

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "provide.foundation.utils.versioning" in name:
                raise ImportError("Module not found")
            # Use the real __import__ for other modules
            import builtins

            return builtins.__import__(name, *args, **kwargs)

        # Temporarily remove versioning from sys.modules if present
        import sys

        versioning_backup = sys.modules.get("provide.foundation.utils.versioning")
        try:
            if "provide.foundation.utils.versioning" in sys.modules:
                del sys.modules["provide.foundation.utils.versioning"]

            with patch("builtins.__import__", side_effect=mock_import):
                version = _get_service_version()
                assert version is None
        finally:
            # Restore module if it was present
            if versioning_backup is not None:
                sys.modules["provide.foundation.utils.versioning"] = versioning_backup

    def test_returns_none_on_generic_exception(self) -> None:
        """Test returns None when get_version raises generic exception."""
        mock_get_version = Mock(side_effect=RuntimeError("Unexpected error"))

        with patch("provide.foundation.utils.versioning.get_version", mock_get_version):
            version = _get_service_version()

            assert version is None


class TestTelemetryConfigBasic(FoundationTestCase):
    """Test TelemetryConfig basic functionality."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_creates_with_defaults(self) -> None:
        """Test creating TelemetryConfig with default values."""
        config = TelemetryConfig()

        assert config.globally_disabled is False
        assert config.tracing_enabled is True
        assert config.metrics_enabled is True
        assert config.otlp_endpoint is None
        assert config.otlp_protocol == "http/protobuf"
        assert config.trace_sample_rate == 1.0

    def test_service_name_factory_is_called(self) -> None:
        """Test service_name factory is called during initialization."""
        with patch.dict("os.environ", {"OTEL_SERVICE_NAME": "test-service"}):
            config = TelemetryConfig()

            assert config.service_name == "test-service"

    def test_service_version_factory_is_called(self) -> None:
        """Test service_version factory is called during initialization."""
        with patch("provide.foundation.utils.versioning.get_version", return_value="2.0.0"):
            config = TelemetryConfig()

            assert config.service_version == "2.0.0"

    def test_get_otlp_headers_dict_returns_headers(self) -> None:
        """Test get_otlp_headers_dict returns headers dictionary."""
        headers = {"key": "value", "auth": "token"}
        config = TelemetryConfig(otlp_headers=headers)

        result = config.get_otlp_headers_dict()

        assert result == headers
        assert result is config.otlp_headers  # Should return the same dict


class TestTelemetryConfigFromEnv(FoundationTestCase):
    """Test TelemetryConfig.from_env() method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_from_env_loads_environment_variables(self) -> None:
        """Test from_env loads configuration from environment variables."""
        with patch.dict(
            "os.environ",
            {
                "PROVIDE_TELEMETRY_DISABLED": "true",
                "OTEL_TRACING_ENABLED": "false",
                "OTEL_METRICS_ENABLED": "false",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4318",
                "OTEL_TRACE_SAMPLE_RATE": "0.5",
            },
        ):
            config = TelemetryConfig.from_env()

            assert config.globally_disabled is True
            assert config.tracing_enabled is False
            assert config.metrics_enabled is False
            assert config.otlp_endpoint == "http://localhost:4318"
            assert config.trace_sample_rate == 0.5

    def test_from_env_skips_auto_configure_when_endpoint_set(self) -> None:
        """Test auto-configure is skipped when OTLP endpoint already set."""
        with patch.dict("os.environ", {"OTEL_EXPORTER_OTLP_ENDPOINT": "http://custom:4318"}):
            with patch.object(
                TelemetryConfig,
                "_auto_configure_openobserve_otlp",
            ) as mock_auto:
                config = TelemetryConfig.from_env()

                # Should not call auto-configure since endpoint is set
                mock_auto.assert_not_called()
                assert config.otlp_endpoint == "http://custom:4318"

    def test_from_env_calls_auto_configure_when_no_endpoint(self) -> None:
        """Test auto-configure is called when no OTLP endpoint set."""
        with (
            patch.dict("os.environ", {}, clear=True),
            patch.object(
                TelemetryConfig,
                "_auto_configure_openobserve_otlp",
                return_value=TelemetryConfig(),
            ) as mock_auto,
        ):
            TelemetryConfig.from_env()

            # Should call auto-configure
            mock_auto.assert_called_once()


class TestAutoConfigureOpenObserveOTLP(FoundationTestCase):
    """Test TelemetryConfig._auto_configure_openobserve_otlp() method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_returns_original_config_on_import_error(self) -> None:
        """Test returns original config when OpenObserve integration unavailable."""
        original_config = TelemetryConfig()

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "provide.foundation.integrations.openobserve.config" in name:
                raise ImportError("Module not found")
            import builtins

            return builtins.__import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert result is original_config

    def test_returns_original_config_when_openobserve_not_configured(self) -> None:
        """Test returns original config when OpenObserve is not configured."""
        original_config = TelemetryConfig()

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = False

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert result is original_config

    def test_returns_original_config_when_no_otlp_endpoint(self) -> None:
        """Test returns original config when OpenObserve has no OTLP endpoint."""
        original_config = TelemetryConfig()

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = None

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert result is original_config

    def test_configures_otlp_endpoint_from_openobserve(self) -> None:
        """Test configures OTLP endpoint from OpenObserve."""
        original_config = TelemetryConfig(otlp_headers={})

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/api/default/v1/traces"
        mock_oo_config.org = None
        mock_oo_config.stream = None
        mock_oo_config.user = None
        mock_oo_config.password = None

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert result.otlp_endpoint == "http://localhost:5080/api/default/v1/traces"

    def test_adds_organization_header_when_available(self) -> None:
        """Test adds organization header to OTLP headers when available."""
        original_config = TelemetryConfig(otlp_headers={})

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/traces"
        mock_oo_config.org = "my-org"
        mock_oo_config.stream = None
        mock_oo_config.user = None
        mock_oo_config.password = None

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert "organization" in result.otlp_headers
            assert result.otlp_headers["organization"] == "my-org"

    def test_adds_stream_header_when_available(self) -> None:
        """Test adds stream-name header to OTLP headers when available."""
        original_config = TelemetryConfig(otlp_headers={})

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/traces"
        mock_oo_config.org = None
        mock_oo_config.stream = "default"
        mock_oo_config.user = None
        mock_oo_config.password = None

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert "stream-name" in result.otlp_headers
            assert result.otlp_headers["stream-name"] == "default"

    def test_adds_basic_auth_header_when_credentials_available(self) -> None:
        """Test adds Basic auth header when user and password available."""
        original_config = TelemetryConfig(otlp_headers={})

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/traces"
        mock_oo_config.org = None
        mock_oo_config.stream = None
        mock_oo_config.user = "admin"
        mock_oo_config.password = "secret123"

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            assert "authorization" in result.otlp_headers
            # Verify Basic auth format
            auth_header = result.otlp_headers["authorization"]
            assert auth_header.startswith("Basic ")

            # Decode and verify credentials
            encoded = auth_header.replace("Basic ", "")
            decoded = base64.b64decode(encoded).decode("ascii")
            assert decoded == "admin:secret123"

    def test_preserves_existing_headers(self) -> None:
        """Test preserves existing OTLP headers while adding new ones."""
        original_config = TelemetryConfig(
            otlp_headers={
                "custom-header": "custom-value",
                "another-header": "another-value",
            },
        )

        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/traces"
        mock_oo_config.org = "my-org"
        mock_oo_config.stream = "default"
        mock_oo_config.user = None
        mock_oo_config.password = None

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            # Original headers should be preserved
            assert result.otlp_headers["custom-header"] == "custom-value"
            assert result.otlp_headers["another-header"] == "another-value"

            # New headers should be added
            assert result.otlp_headers["organization"] == "my-org"
            assert result.otlp_headers["stream-name"] == "default"

    def test_returns_original_config_on_generic_exception(self) -> None:
        """Test returns original config when generic exception occurs."""
        original_config = TelemetryConfig()

        mock_oo_config = Mock()
        mock_oo_config.is_configured.side_effect = RuntimeError("Unexpected error")

        with patch(
            "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
            return_value=mock_oo_config,
        ):
            result = TelemetryConfig._auto_configure_openobserve_otlp(original_config)

            # Should return original config without raising
            assert result is original_config


class TestTelemetryConfigIntegration(FoundationTestCase):
    """Test TelemetryConfig integration scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_from_env_with_full_openobserve_auto_config(self) -> None:
        """Test from_env with full OpenObserve auto-configuration."""
        mock_oo_config = Mock()
        mock_oo_config.is_configured.return_value = True
        mock_oo_config.get_otlp_endpoint.return_value = "http://localhost:5080/api/default/v1/traces"
        mock_oo_config.org = "test-org"
        mock_oo_config.stream = "test-stream"
        mock_oo_config.user = "user"
        mock_oo_config.password = "pass"

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "provide.foundation.integrations.openobserve.config.OpenObserveConfig.from_env",
                return_value=mock_oo_config,
            ),
        ):
            config = TelemetryConfig.from_env()

            # Should have auto-configured OTLP
            assert config.otlp_endpoint == "http://localhost:5080/api/default/v1/traces"
            assert config.otlp_headers["organization"] == "test-org"
            assert config.otlp_headers["stream-name"] == "test-stream"
            assert "authorization" in config.otlp_headers

    def test_from_env_with_manual_and_auto_config(self) -> None:
        """Test that manual config takes precedence over auto-config."""
        with patch.dict("os.environ", {"OTEL_EXPORTER_OTLP_ENDPOINT": "http://manual:4318"}):
            config = TelemetryConfig.from_env()

            # Should use manual endpoint, not auto-configure
            assert config.otlp_endpoint == "http://manual:4318"


__all__ = [
    "TestAutoConfigureOpenObserveOTLP",
    "TestGetServiceName",
    "TestGetServiceVersion",
    "TestTelemetryConfigBasic",
    "TestTelemetryConfigFromEnv",
    "TestTelemetryConfigIntegration",
]

# 🧱🏗️🔚
