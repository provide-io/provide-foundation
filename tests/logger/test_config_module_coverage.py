#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger/config.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase


class TestLoggerConfigModule(FoundationTestCase):
    """Test the logger config module re-exports."""

    def test_module_imports(self) -> None:
        """Test that the module can be imported."""
        # Direct import of the config module
        from provide.foundation.logger import config

        assert config is not None
        assert hasattr(config, "LoggingConfig")
        assert hasattr(config, "TelemetryConfig")

    def test_logging_config_export(self) -> None:
        """Test LoggingConfig is properly exported."""
        from provide.foundation.logger.config import LoggingConfig

        assert LoggingConfig is not None

        # Verify it's the actual class
        config = LoggingConfig()
        assert hasattr(config, "default_level")
        assert hasattr(config, "console_formatter")

    def test_telemetry_config_export(self) -> None:
        """Test TelemetryConfig is properly exported."""
        from provide.foundation.logger.config import TelemetryConfig

        assert TelemetryConfig is not None

        # Verify it's the actual class
        config = TelemetryConfig()
        assert hasattr(config, "logging")
        assert hasattr(config, "service_name")

    def test_all_exports(self) -> None:
        """Test __all__ exports are correct."""
        from provide.foundation.logger import config as config_module

        assert hasattr(config_module, "__all__")
        assert "LoggingConfig" in config_module.__all__
        assert "TelemetryConfig" in config_module.__all__
        assert len(config_module.__all__) == 2

    def test_re_export_consistency(self) -> None:
        """Test that re-exported classes match original imports."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
        from provide.foundation.logger.config.logging import (
            LoggingConfig as OrigLoggingConfig,
        )
        from provide.foundation.logger.config.telemetry import (
            TelemetryConfig as OrigTelemetryConfig,
        )

        # They should be the exact same class objects
        assert LoggingConfig is OrigLoggingConfig
        assert TelemetryConfig is OrigTelemetryConfig

    def test_import_all_star(self) -> None:
        """Test star import works correctly."""
        # This tests that __all__ is properly configured
        exec_globals = {}
        exec("from provide.foundation.logger.config import *", exec_globals)

        assert "LoggingConfig" in exec_globals
        assert "TelemetryConfig" in exec_globals
        # Should only import what's in __all__
        assert len([k for k in exec_globals if not k.startswith("__")]) == 2


# 🧱🏗️🔚
