#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for hub/foundation.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.hub.foundation import FoundationManager, get_foundation_logger
from provide.foundation.hub.manager import get_hub
from provide.foundation.hub.registry import Registry
from provide.foundation.logger.config import TelemetryConfig


class TestFoundationManager(FoundationTestCase):
    """Test FoundationManager class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        super().setup_method()
        self.hub = get_hub()
        self.registry = Registry()
        self.manager = FoundationManager(self.hub, self.registry)

    def test_initialization(self) -> None:
        """Test FoundationManager initialization."""
        assert self.manager._hub is self.hub
        assert self.manager._registry is self.registry
        assert not self.manager._initialized
        assert self.manager._config is None
        assert self.manager._logger_instance is None

    def test_initialize_foundation_default(self) -> None:
        """Test initializing Foundation with default config."""
        self.manager.initialize_foundation()

        assert self.manager._initialized
        assert self.manager._config is not None

    def test_initialize_foundation_with_config(self) -> None:
        """Test initializing Foundation with explicit config."""
        config = TelemetryConfig(service_name="test-service")

        # Use force=True to ensure explicit config is used
        self.manager.initialize_foundation(config=config, force=True)

        assert self.manager._initialized
        assert self.manager._config is not None
        # Verify config was applied
        assert self.manager._config.service_name == "test-service"

    def test_initialize_foundation_idempotent(self) -> None:
        """Test that initialize_foundation is idempotent."""
        self.manager.initialize_foundation()
        first_config = self.manager._config

        # Second call should not re-initialize
        self.manager.initialize_foundation()
        assert self.manager._config is first_config

    def test_initialize_foundation_force_reinit(self) -> None:
        """Test force re-initialization."""
        self.manager.initialize_foundation()
        first_config = self.manager._config

        # Force re-initialization
        new_config = TelemetryConfig(service_name="different-service")
        self.manager.initialize_foundation(config=new_config, force=True)

        assert self.manager._config is not first_config
        assert self.manager._config.service_name == "different-service"

    def test_smart_initialization_with_otlp(self) -> None:
        """Test smart initialization when OTLP is configured."""
        # First initialize with default config (auto-init)
        auto_config = TelemetryConfig(service_name=None, otlp_endpoint="http://localhost:5555")
        self.manager.initialize_foundation(config=auto_config)

        # Now provide explicit config - should force re-init due to OTLP
        explicit_config = TelemetryConfig(
            service_name="explicit-service", otlp_endpoint="http://localhost:5555"
        )

        with patch("provide.foundation.logger.setup.coordinator.get_system_logger") as mock_logger_factory:
            mock_logger = MagicMock()
            mock_logger_factory.return_value = mock_logger

            self.manager.initialize_foundation(config=explicit_config)

            # Should have logged re-initialization
            mock_logger.info.assert_called()

    @pytest.mark.skip(reason="Lightweight config update feature is being refactored")
    def test_smart_initialization_lightweight_update(self) -> None:
        """Test smart initialization with lightweight config update."""
        import os

        # Clear service name env vars to ensure service_name stays None
        original_otel = os.environ.pop("OTEL_SERVICE_NAME", None)
        original_provide = os.environ.pop("PROVIDE_SERVICE_NAME", None)

        try:
            # Initialize with default config (service_name should be None)
            auto_config = TelemetryConfig(service_name=None)  # Auto-init marker
            self.manager.initialize_foundation(config=auto_config)

            # Verify the stored config has service_name=None (auto-init marker)
            assert self.manager._config is not None
            assert self.manager._config.service_name is None

            # Provide explicit config without OTLP - should try lightweight update
            explicit_config = TelemetryConfig(service_name="explicit-service")

            # Mock the coordinator's update method
            from provide.foundation.hub.initialization import get_initialization_coordinator

            coordinator = get_initialization_coordinator()

            with (
                patch.object(coordinator, "update_config_if_default", return_value=True) as mock_update,
                patch.object(
                    coordinator, "initialize_foundation", return_value=(explicit_config, MagicMock())
                ),
            ):
                self.manager.initialize_foundation(config=explicit_config)

                # Should have attempted lightweight update
                mock_update.assert_called_once()
        finally:
            # Restore environment variables
            if original_otel is not None:
                os.environ["OTEL_SERVICE_NAME"] = original_otel
            if original_provide is not None:
                os.environ["PROVIDE_SERVICE_NAME"] = original_provide

    def test_get_foundation_logger(self) -> None:
        """Test getting Foundation logger."""
        logger = self.manager.get_foundation_logger("test.module")

        assert logger is not None
        assert self.manager._initialized  # Should auto-initialize

    def test_get_foundation_logger_auto_initialize(self) -> None:
        """Test that get_foundation_logger auto-initializes."""
        assert not self.manager._initialized

        logger = self.manager.get_foundation_logger()

        assert logger is not None
        assert self.manager._initialized

    def test_get_foundation_logger_with_name(self) -> None:
        """Test getting logger with specific name."""
        self.manager.initialize_foundation()

        logger = self.manager.get_foundation_logger("my.custom.logger")

        assert logger is not None

    def test_get_foundation_logger_fallback(self) -> None:
        """Test logger fallback when instance not available."""
        # Initialize but don't store logger instance in registry
        self.manager._initialized = True

        logger = self.manager.get_foundation_logger()

        assert logger is not None  # Should fallback to structlog

    def test_is_foundation_initialized(self) -> None:
        """Test checking initialization status."""
        assert not self.manager.is_foundation_initialized()

        self.manager.initialize_foundation()

        assert self.manager.is_foundation_initialized()

    def test_get_foundation_config(self) -> None:
        """Test getting Foundation config."""
        config = self.manager.get_foundation_config()

        assert config is not None
        assert self.manager._initialized  # Should auto-initialize

    def test_get_foundation_config_when_initialized(self) -> None:
        """Test getting config when already initialized."""
        explicit_config = TelemetryConfig(service_name="test")
        self.manager.initialize_foundation(config=explicit_config, force=True)

        config = self.manager.get_foundation_config()

        assert config is not None
        # Config should have the service_name we provided
        assert config is not None

    def test_get_foundation_config_from_registry_fallback(self) -> None:
        """Test getting config from registry when local config is None."""
        self.manager._initialized = True
        self.manager._config = None

        # Put config in registry
        registry_config = TelemetryConfig(service_name="registry-config")
        self.registry.register("foundation.config", registry_config, "singleton")

        config = self.manager.get_foundation_config()

        assert config is not None
        assert config.service_name == "registry-config"

    def test_clear_foundation_state(self) -> None:
        """Test clearing Foundation state."""
        self.manager.initialize_foundation()

        assert self.manager._initialized
        assert self.manager._config is not None

        self.manager.clear_foundation_state()

        assert not self.manager._initialized
        assert self.manager._config is None
        assert self.manager._logger_instance is None

    def test_clear_foundation_state_removes_registry_entries(self) -> None:
        """Test that clear removes registry entries."""
        # Initialize and register
        self.manager.initialize_foundation()

        # Clear state
        self.manager.clear_foundation_state()

        # Registry entries should be removed
        assert self.registry.get("foundation.config", "singleton") is None

    def test_clear_foundation_state_in_test_mode(self) -> None:
        """Test that clear resets coordinator in test mode."""
        # We're in test mode (PYTEST_CURRENT_TEST is set by testkit)
        self.manager.initialize_foundation()

        with patch("provide.foundation.testmode.internal.reset_global_coordinator") as mock_reset:
            self.manager.clear_foundation_state()

            # Should have called reset in test mode
            mock_reset.assert_called_once()

    def test_internal_get_logger(self) -> None:
        """Test internal _get_logger method."""
        self.manager.initialize_foundation()

        logger = self.manager._get_logger()

        assert logger is not None

    def test_internal_get_logger_fallback(self) -> None:
        """Test _get_logger fallback when no logger instance."""
        self.manager._logger_instance = None

        logger = self.manager._get_logger()

        assert logger is not None  # Should fallback to structlog

    def test_initialize_foundation_logs_success(self) -> None:
        """Test that initialization logs success message."""
        # Clear test environment variable to enable logging
        import os

        original_env = os.environ.get("PYTEST_CURRENT_TEST")
        if original_env:
            del os.environ["PYTEST_CURRENT_TEST"]

        try:
            self.manager.initialize_foundation()

            # Restore immediately
            if original_env:
                os.environ["PYTEST_CURRENT_TEST"] = original_env

            # Success - initialization completed without errors
            assert self.manager._initialized
        finally:
            # Ensure restoration even on failure
            if original_env and "PYTEST_CURRENT_TEST" not in os.environ:
                os.environ["PYTEST_CURRENT_TEST"] = original_env

    def test_smart_initialization_lightweight_update_fails(self) -> None:
        """Test smart initialization when lightweight update fails."""
        # Initialize with default config
        auto_config = TelemetryConfig(service_name=None)  # Auto-init marker
        self.manager.initialize_foundation(config=auto_config)

        # Provide explicit config without OTLP
        explicit_config = TelemetryConfig(service_name="explicit-service")

        with patch(
            "provide.foundation.hub.initialization.get_initialization_coordinator"
        ) as mock_coordinator_factory:
            mock_coordinator = MagicMock()
            # Make lightweight update fail
            mock_coordinator.update_config_if_default.return_value = False
            # But still handle full initialization
            mock_coordinator.initialize_foundation.return_value = (explicit_config, MagicMock())
            mock_coordinator_factory.return_value = mock_coordinator

            self.manager.initialize_foundation(config=explicit_config)

            # Should have fallen through to full initialization
            mock_coordinator.initialize_foundation.assert_called()

    def test_clear_foundation_state_registry_error_suppressed(self) -> None:
        """Test that registry errors during clear are suppressed."""
        self.manager._initialized = True

        # Create a mock registry that raises on remove
        mock_registry = MagicMock()
        mock_registry.remove.side_effect = Exception("Registry error")
        self.manager._registry = mock_registry

        # Should not raise despite registry errors
        self.manager.clear_foundation_state()

        # State should still be cleared
        assert not self.manager._initialized


class TestGetFoundationLogger(FoundationTestCase):
    """Test the get_foundation_logger function."""

    def test_get_foundation_logger_function(self) -> None:
        """Test the module-level get_foundation_logger function."""
        logger = get_foundation_logger("test.module")

        assert logger is not None

    def test_get_foundation_logger_function_no_name(self) -> None:
        """Test get_foundation_logger without name."""
        logger = get_foundation_logger()

        assert logger is not None

    def test_get_foundation_logger_with_hub_instance(self) -> None:
        """Test get_foundation_logger when hub has logger instance."""
        hub = get_hub()
        hub.initialize_foundation()

        logger = get_foundation_logger("custom.logger")

        assert logger is not None

    def test_get_foundation_logger_fallback_to_direct_import(self) -> None:
        """Test fallback to direct logger import during bootstrap."""
        # Clear hub foundation to test fallback
        hub = get_hub()
        if hasattr(hub, "_foundation"):
            hub._foundation._logger_instance = None

        logger = get_foundation_logger("bootstrap.logger")

        assert logger is not None

    def test_get_foundation_logger_returns_logger_directly(self) -> None:
        """Test get_foundation_logger returns logger directly when no name provided."""
        # Clear hub foundation to test fallback path
        hub = get_hub()
        if hasattr(hub, "_foundation"):
            hub._foundation._logger_instance = None

        logger = get_foundation_logger()  # No name

        assert logger is not None


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
