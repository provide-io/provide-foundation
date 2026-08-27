#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Foundation's setup logger must survive a broken environment.

The setup logger is built before the configuration is initialized, so an
unguarded `TelemetryConfig.from_env()` in the coordinator turned one malformed
environment variable into a failure to start -- defeating the fallback that
`FoundationInitializer._initialize_config` already provided one layer up."""

from __future__ import annotations

import logging as stdlib_logging

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.logger.setup.coordinator import (
    get_foundation_log_level,
    reset_foundation_log_level_cache,
)


class TestCoordinatorConfigFallback(FoundationTestCase):
    """A from_env failure degrades to defaults rather than propagating."""

    def setup_method(self) -> None:
        super().setup_method()
        reset_foundation_log_level_cache()

    def teardown_method(self) -> None:
        reset_foundation_log_level_cache()
        super().teardown_method()

    def test_env_failure_falls_back_to_default_level(self) -> None:
        """A cold cache plus a raising from_env must not abort setup."""
        from provide.foundation.logger.config import TelemetryConfig

        # Derived rather than hardcoded: the point is that the fallback lands on
        # whatever a default TelemetryConfig says, not on one particular level.
        expected = get_foundation_log_level(TelemetryConfig())
        reset_foundation_log_level_cache()

        with patch(
            "provide.foundation.logger.config.TelemetryConfig.from_env",
            side_effect=Exception("Config error"),
        ):
            level = get_foundation_log_level()

        assert level == expected

    def test_import_errors_still_propagate(self) -> None:
        """A broken package is not a broken environment and must not be masked."""
        with (
            patch(
                "provide.foundation.logger.config.TelemetryConfig.from_env",
                side_effect=Exception("cannot import name 'thing'"),
            ),
            pytest.raises(Exception, match="cannot import"),
        ):
            get_foundation_log_level()

    def test_explicit_config_bypasses_the_environment(self) -> None:
        """A caller-supplied config never touches from_env at all."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        config = TelemetryConfig(logging=LoggingConfig(foundation_setup_log_level="DEBUG"))
        with patch(
            "provide.foundation.logger.config.TelemetryConfig.from_env",
            side_effect=AssertionError("from_env must not be called"),
        ):
            level = get_foundation_log_level(config)

        assert level == stdlib_logging.DEBUG


# 🧱🏗️🔚
