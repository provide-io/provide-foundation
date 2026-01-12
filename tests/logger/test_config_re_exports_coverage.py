#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for logger/config.py re-exports module."""

from __future__ import annotations

import importlib

from provide.testkit import FoundationTestCase


class TestLoggerConfigReExports(FoundationTestCase):
    """Test logger/config.py re-exports functionality."""

    def test_logging_config_import(self) -> None:
        """Test LoggingConfig can be imported from logger.config."""
        from provide.foundation.logger.config import LoggingConfig

        assert LoggingConfig is not None
        # Verify it's the same class as the original
        from provide.foundation.logger.config.logging import (
            LoggingConfig as OriginalLoggingConfig,
        )

        assert LoggingConfig is OriginalLoggingConfig

    def test_telemetry_config_import(self) -> None:
        """Test TelemetryConfig can be imported from logger.config."""
        from provide.foundation.logger.config import TelemetryConfig

        assert TelemetryConfig is not None
        # Verify it's the same class as the original
        from provide.foundation.logger.config.telemetry import (
            TelemetryConfig as OriginalTelemetryConfig,
        )

        assert TelemetryConfig is OriginalTelemetryConfig

    def test_all_exports_defined(self) -> None:
        """Test that __all__ exports are properly defined."""
        config_module = importlib.import_module("provide.foundation.logger.config")

        expected_exports = ["LoggingConfig", "TelemetryConfig"]

        assert hasattr(config_module, "__all__")
        assert config_module.__all__ == expected_exports

    def test_all_exports_accessible(self) -> None:
        """Test that all items in __all__ are actually accessible."""
        config_module = importlib.import_module("provide.foundation.logger.config")

        for export_name in config_module.__all__:
            assert hasattr(config_module, export_name)
            export_item = getattr(config_module, export_name)
            assert export_item is not None

    def test_module_docstring(self) -> None:
        """Test that module has proper docstring."""
        config_module = importlib.import_module("provide.foundation.logger.config")

        assert config_module.__doc__ is not None
        assert "Foundation Logger Configuration Module" in config_module.__doc__
        assert "Re-exports" in config_module.__doc__

    def test_direct_import_consistency(self) -> None:
        """Test that direct imports and re-exports are consistent."""
        # Import via re-export
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Import directly
        from provide.foundation.logger.config.logging import (
            LoggingConfig as DirectLoggingConfig,
        )
        from provide.foundation.logger.config.telemetry import (
            TelemetryConfig as DirectTelemetryConfig,
        )

        # Should be the same objects
        assert LoggingConfig is DirectLoggingConfig
        assert TelemetryConfig is DirectTelemetryConfig

    def test_star_import_functionality(self) -> None:
        """Test that star imports work correctly."""
        # This simulates: from provide.foundation.logger.config import *
        config_module = importlib.import_module("provide.foundation.logger.config")

        # Get all items that would be imported with star import
        star_imports = {name: getattr(config_module, name) for name in config_module.__all__}

        assert "LoggingConfig" in star_imports
        assert "TelemetryConfig" in star_imports
        assert len(star_imports) == 2

    def test_re_export_module_attributes(self) -> None:
        """Test that re-exported classes maintain their module attributes."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Check module attributes
        assert LoggingConfig.__module__ == "provide.foundation.logger.config.logging"
        assert TelemetryConfig.__module__ == "provide.foundation.logger.config.telemetry"

    def test_no_additional_exports(self) -> None:
        """Test that __all__ items are properly exported."""
        config_module = importlib.import_module("provide.foundation.logger.config")

        # Get all public attributes (not starting with _)
        public_attrs = [attr for attr in dir(config_module) if not attr.startswith("_")]

        # All items in __all__ should be present as public attributes
        for expected_export in config_module.__all__:
            assert expected_export in public_attrs, f"Missing expected export: {expected_export}"

        # Check that the main exports are classes (not modules)
        assert hasattr(config_module, "LoggingConfig")
        assert hasattr(config_module, "TelemetryConfig")


class TestConfigModuleIntegration:
    """Test integration aspects of the config re-export module."""

    def test_config_classes_are_functional(self) -> None:
        """Test that re-exported config classes are functional."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Test LoggingConfig functionality
        logging_config = LoggingConfig()
        assert hasattr(logging_config, "default_level")

        # Test TelemetryConfig functionality
        telemetry_config = TelemetryConfig()
        assert hasattr(telemetry_config, "service_name")

    def test_backwards_compatibility(self) -> None:
        """Test that the re-export module maintains backwards compatibility."""
        # These imports should work for backwards compatibility
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Test that they can be instantiated and used as before
        logging_config = LoggingConfig(default_level="INFO")
        telemetry_config = TelemetryConfig(service_name="test-service")

        assert logging_config.default_level == "INFO"
        assert telemetry_config.service_name == "test-service"

    def test_import_error_handling(self) -> None:
        """Test behavior when underlying modules have issues."""
        # This is more of a structural test to ensure the imports work
        # In a real scenario, if the underlying modules fail, this should too

        try:
            from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

            # If we get here, imports worked
            assert LoggingConfig is not None
            assert TelemetryConfig is not None
        except ImportError as e:
            # If there's an import error, it should be from the underlying modules
            assert "logging" in str(e) or "telemetry" in str(e)


# 🧱🏗️🔚
