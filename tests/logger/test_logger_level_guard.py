#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for level guards, FilteringBoundLogger integration, and is_*_enabled helpers."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from provide.testkit import FoundationTestCase

from provide.foundation.logger.core import (
    _DEBUG_LEVEL,
    _LEVEL_TO_NUMERIC,
    _TRACE_LEVEL,
    FoundationLogger,
    GlobalLoggerProxy,
    is_debug_enabled,
    is_trace_enabled,
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


class TestGlobalLoggerProxyForwarding(FoundationTestCase):
    """Test that GlobalLoggerProxy forwards all methods.

    With FilteringBoundLogger as wrapper_class, methods below the configured
    level are literal ``return None`` at the structlog layer.  The proxy no
    longer needs its own guards — it simply forwards to FoundationLogger.
    """

    def test_debug_always_forwarded(self) -> None:
        """debug() should always forward (FilteringBoundLogger handles filtering)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 20  # INFO — previously would have been skipped

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("this forwards now", key="value")

        mock_logger.debug.assert_called_once_with("this forwards now", key="value")

    def test_trace_always_forwarded(self) -> None:
        """trace() should always forward (FilteringBoundLogger handles filtering)."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 10  # DEBUG — previously would have been skipped

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.trace("this forwards now", extra="data")

        mock_logger.trace.assert_called_once_with("this forwards now", extra="data")

    def test_debug_forwarded_at_debug_level(self) -> None:
        """debug() forwards when effective level is DEBUG."""
        proxy = GlobalLoggerProxy()

        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger._effective_level = 10  # DEBUG

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            proxy.debug("this should pass", key="value")

        mock_logger.debug.assert_called_once_with("this should pass", key="value")

    def test_trace_forwarded_at_trace_level(self) -> None:
        """trace() forwards when effective level is TRACE."""
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


class TestIsDebugEnabled(FoundationTestCase):
    """Test is_debug_enabled() and is_trace_enabled() on both classes."""

    def test_foundation_logger_is_debug_enabled_at_debug(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 10  # DEBUG
        assert logger.is_debug_enabled() is True

    def test_foundation_logger_is_debug_enabled_at_info(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 20  # INFO
        assert logger.is_debug_enabled() is False

    def test_foundation_logger_is_debug_enabled_at_trace(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 5  # TRACE
        assert logger.is_debug_enabled() is True

    def test_foundation_logger_is_debug_enabled_unconfigured(self) -> None:
        """Unconfigured (level 0) should return True — let everything through."""
        logger = FoundationLogger()
        assert logger._effective_level == 0
        assert logger.is_debug_enabled() is True

    def test_foundation_logger_is_trace_enabled_at_trace(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 5
        assert logger.is_trace_enabled() is True

    def test_foundation_logger_is_trace_enabled_at_debug(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 10
        assert logger.is_trace_enabled() is False

    def test_foundation_logger_is_trace_enabled_at_info(self) -> None:
        logger = FoundationLogger()
        logger._effective_level = 20
        assert logger.is_trace_enabled() is False

    def test_proxy_is_debug_enabled(self) -> None:
        proxy = GlobalLoggerProxy()
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_debug_enabled.return_value = False

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            result = proxy.is_debug_enabled()

        assert result is False
        mock_logger.is_debug_enabled.assert_called_once()

    def test_proxy_is_trace_enabled(self) -> None:
        proxy = GlobalLoggerProxy()
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_trace_enabled.return_value = True

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            result = proxy.is_trace_enabled()

        assert result is True
        mock_logger.is_trace_enabled.assert_called_once()


class TestStandaloneHelpers(FoundationTestCase):
    """Test standalone is_debug_enabled() and is_trace_enabled() functions."""

    def test_standalone_is_debug_enabled_true(self) -> None:
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_debug_enabled.return_value = True

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            assert is_debug_enabled() is True

    def test_standalone_is_debug_enabled_false(self) -> None:
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_debug_enabled.return_value = False

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            assert is_debug_enabled() is False

    def test_standalone_is_trace_enabled_true(self) -> None:
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_trace_enabled.return_value = True

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            assert is_trace_enabled() is True

    def test_standalone_is_trace_enabled_false(self) -> None:
        mock_logger = MagicMock(spec=FoundationLogger)
        mock_logger.is_trace_enabled.return_value = False

        with patch("provide.foundation.logger.core.get_global_logger", return_value=mock_logger):
            assert is_trace_enabled() is False


# 🧱🏗️🔚
