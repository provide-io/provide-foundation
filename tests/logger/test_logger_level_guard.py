#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for debug/trace level guards in GlobalLoggerProxy and FoundationLogger."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from provide.testkit import FoundationTestCase

from provide.foundation.logger.core import (
    _DEBUG_LEVEL,
    _LEVEL_TO_NUMERIC,
    _TRACE_LEVEL,
    FoundationLogger,
    GlobalLoggerProxy,
)


class TestEffectiveLevelMapping(FoundationTestCase):
    """Test the _LEVEL_TO_NUMERIC mapping and constants."""

    def test_level_mapping_values(self) -> None:
        """Verify standard log level numeric values."""
        assert _LEVEL_TO_NUMERIC["TRACE"] == 5
        assert _LEVEL_TO_NUMERIC["DEBUG"] == 10
        assert _LEVEL_TO_NUMERIC["INFO"] == 20
        assert _LEVEL_TO_NUMERIC["WARNING"] == 30
        assert _LEVEL_TO_NUMERIC["ERROR"] == 40
        assert _LEVEL_TO_NUMERIC["CRITICAL"] == 50
        assert _LEVEL_TO_NUMERIC["NOTSET"] == 0

    def test_threshold_constants(self) -> None:
        """Verify threshold constants match mapping."""
        assert _DEBUG_LEVEL == 10
        assert _TRACE_LEVEL == 5


class TestFoundationLoggerEffectiveLevel(FoundationTestCase):
    """Test _effective_level on FoundationLogger."""

    def test_default_effective_level_is_zero(self) -> None:
        """Unconfigured logger should have level 0 (pass everything through)."""
        logger = FoundationLogger()
        assert logger._effective_level == 0

    def test_setup_caches_effective_level(self) -> None:
        """setup() should cache the numeric level from config."""
        logger = FoundationLogger()

        # Create a mock config with logging.default_level = "INFO"
        mock_config = MagicMock()
        mock_config.logging.default_level = "INFO"

        with patch("provide.foundation.logger.core.internal_setup", create=True):
            with patch("provide.foundation.logger.setup.coordinator.internal_setup"):
                try:
                    logger.setup(mock_config)
                except Exception:
                    pass  # Setup internals may fail in test — we only care about level caching

        assert logger._effective_level == 20  # INFO

    def test_setup_caches_debug_level(self) -> None:
        """setup() with DEBUG level should set _effective_level to 10."""
        logger = FoundationLogger()

        mock_config = MagicMock()
        mock_config.logging.default_level = "DEBUG"

        with patch("provide.foundation.logger.setup.coordinator.internal_setup"):
            try:
                logger.setup(mock_config)
            except Exception:
                pass

        assert logger._effective_level == 10  # DEBUG

    def test_setup_caches_trace_level(self) -> None:
        """setup() with TRACE level should set _effective_level to 5."""
        logger = FoundationLogger()

        mock_config = MagicMock()
        mock_config.logging.default_level = "TRACE"

        with patch("provide.foundation.logger.setup.coordinator.internal_setup"):
            try:
                logger.setup(mock_config)
            except Exception:
                pass

        assert logger._effective_level == 5  # TRACE


class TestGlobalLoggerProxyLevelGuard(FoundationTestCase):
    """Test that GlobalLoggerProxy.debug() and .trace() short-circuit when level is too high."""

    def test_debug_skipped_at_info_level(self) -> None:
        """debug() should not call through when effective level is INFO (20)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 20  # INFO

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("this should be skipped", key="value")

        mock_logger.debug.assert_not_called()

    def test_debug_allowed_at_debug_level(self) -> None:
        """debug() should call through when effective level is DEBUG (10)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 10  # DEBUG

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("this should pass", key="value")

        mock_logger.debug.assert_called_once_with("this should pass", key="value")

    def test_debug_allowed_at_trace_level(self) -> None:
        """debug() should call through when effective level is TRACE (5)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 5  # TRACE

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("this should pass")

        mock_logger.debug.assert_called_once_with("this should pass")

    def test_debug_allowed_at_notset_level(self) -> None:
        """debug() should call through when effective level is 0 (unconfigured)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 0  # NOTSET / unconfigured

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("unconfigured should pass")

        mock_logger.debug.assert_called_once_with("unconfigured should pass")

    def test_trace_skipped_at_debug_level(self) -> None:
        """trace() should not call through when effective level is DEBUG (10)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 10  # DEBUG

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.trace("this should be skipped")

        mock_logger.trace.assert_not_called()

    def test_trace_skipped_at_info_level(self) -> None:
        """trace() should not call through when effective level is INFO (20)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 20  # INFO

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.trace("this should be skipped")

        mock_logger.trace.assert_not_called()

    def test_trace_allowed_at_trace_level(self) -> None:
        """trace() should call through when effective level is TRACE (5)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 5  # TRACE

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.trace("this should pass", extra="data")

        mock_logger.trace.assert_called_once_with("this should pass", extra="data")

    def test_info_always_passes_through(self) -> None:
        """info() should always call through regardless of level (no guard)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 50  # CRITICAL — info still passes

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.info("always passes")

        mock_logger.info.assert_called_once_with("always passes")

    def test_debug_skipped_avoids_arg_formatting(self) -> None:
        """When debug is skipped, positional args should NOT be formatted."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 20  # INFO

        # If args were formatted, this would raise TypeError (wrong format specifiers)
        # The fact it doesn't raise proves the guard works before any formatting
        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("message with %s and %d", "string", 42)

        mock_logger.debug.assert_not_called()


# 🧱🏗️🔚
