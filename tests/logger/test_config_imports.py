#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test coverage for logger config module imports."""

from __future__ import annotations

from provide.testkit import FoundationTestCase


class TestLoggerConfigImports(FoundationTestCase):
    """Test logger config module import functionality."""

    def test_logging_config_import(self) -> None:
        """Test LoggingConfig can be imported from config module."""
        from provide.foundation.logger.config import LoggingConfig

        # Verify it's importable
        assert LoggingConfig is not None
        assert hasattr(LoggingConfig, "__name__")

    def test_telemetry_config_import(self) -> None:
        """Test TelemetryConfig can be imported from config module."""
        from provide.foundation.logger.config import TelemetryConfig

        # Verify it's importable
        assert TelemetryConfig is not None
        assert hasattr(TelemetryConfig, "__name__")

    def test_both_classes_importable_together(self) -> None:
        """Test both config classes can be imported in single statement."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Verify both are importable together
        assert LoggingConfig is not None
        assert TelemetryConfig is not None

        # Verify they're different classes
        assert LoggingConfig is not TelemetryConfig

    def test_star_import_works(self) -> None:
        """Test star import functionality."""
        # This tests the __all__ export functionality
        exec("from provide.foundation.logger.config import *")

        # The star import should have worked without error
        # and made the expected names available in local scope


# 🧱🏗️🔚
