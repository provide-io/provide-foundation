#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for stream utilities to improve code coverage."""

from __future__ import annotations

import io
import sys

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.utils.streams import (
    get_foundation_log_stream,
    get_safe_stderr,
)


class TestStreamsCoverage(FoundationTestCase):
    """Test stream utilities for improved coverage."""

    def test_get_safe_stderr_normal_case(self) -> None:
        """Test get_safe_stderr returns sys.stderr normally."""
        stream = get_safe_stderr()
        assert stream is sys.stderr

    def test_get_safe_stderr_fallback_when_stderr_none(self) -> None:
        """Test get_safe_stderr fallback when sys.stderr is None."""
        original_stderr = sys.stderr
        try:
            sys.stderr = None
            stream = get_safe_stderr()
            assert isinstance(stream, io.StringIO)
        finally:
            sys.stderr = original_stderr

    def test_get_safe_stderr_fallback_when_hasattr_false(self) -> None:
        """Test get_safe_stderr fallback when hasattr returns False."""
        # Mock hasattr to return False for 'stderr' attribute
        with patch("builtins.hasattr") as mock_hasattr:

            def hasattr_side_effect(obj, attr) -> bool:
                return not (obj is sys and attr == "stderr")

            mock_hasattr.side_effect = hasattr_side_effect
            stream = get_safe_stderr()
            assert isinstance(stream, io.StringIO)

    def test_get_foundation_log_stream_stdout(self) -> None:
        """Test get_foundation_log_stream with stdout setting."""
        stream = get_foundation_log_stream("stdout")
        assert stream is sys.stdout

    def test_get_foundation_log_stream_stderr(self) -> None:
        """Test get_foundation_log_stream with stderr setting."""
        stream = get_foundation_log_stream("stderr")
        assert stream is sys.stderr

    def test_get_foundation_log_stream_main_success(self) -> None:
        """Test get_foundation_log_stream with main setting - success case."""
        mock_stream = Mock()

        # Mock the import by patching the import itself
        with patch.dict("sys.modules", {"provide.foundation.streams": Mock()}):
            mock_module = sys.modules["provide.foundation.streams"]
            mock_module.get_log_stream = Mock(return_value=mock_stream)

            stream = get_foundation_log_stream("main")
            assert stream is mock_stream
            mock_module.get_log_stream.assert_called_once()

    def test_get_foundation_log_stream_main_import_error(self) -> None:
        """Test get_foundation_log_stream with main setting - ImportError fallback."""
        # Force ImportError by removing the module from sys.modules if it exists
        original_modules = sys.modules.copy()

        # Remove the module to simulate ImportError
        if "provide.foundation.streams" in sys.modules:
            del sys.modules["provide.foundation.streams"]

        try:
            stream = get_foundation_log_stream("main")
            # Should fallback to safe stderr
            assert stream is sys.stderr
        finally:
            # Restore original modules
            sys.modules.clear()
            sys.modules.update(original_modules)

    def test_get_foundation_log_stream_invalid_value_with_logger(self) -> None:
        """Test get_foundation_log_stream with invalid value and logger available."""
        mock_logger = Mock()

        # Mock the logger module import
        with patch.dict("sys.modules", {"provide.foundation.logger.config.base": Mock()}):
            mock_config_module = sys.modules["provide.foundation.logger.config.base"]
            mock_config_module.get_config_logger = Mock(return_value=mock_logger)

            stream = get_foundation_log_stream("invalid_setting")

            # Should log warning and return stderr
            assert stream is sys.stderr
            mock_config_module.get_config_logger.assert_called_once()
            mock_logger.warning.assert_called_once()

            # Check warning message content
            call_args = mock_logger.warning.call_args
            assert "Invalid FOUNDATION_LOG_OUTPUT value" in call_args[0][0]
            assert call_args[1]["invalid_value"] == "invalid_setting"
            assert call_args[1]["valid_options"] == ["stderr", "stdout", "main"]
            assert call_args[1]["default_used"] == "stderr"

    def test_get_foundation_log_stream_invalid_value_no_logger(self) -> None:
        """Test get_foundation_log_stream with invalid value and no logger available."""
        # Remove the config module to simulate ImportError
        original_modules = sys.modules.copy()

        if "provide.foundation.logger.config" in sys.modules:
            del sys.modules["provide.foundation.logger.config"]

        try:
            stream = get_foundation_log_stream("invalid_setting")
            # Should silently fallback to stderr without warning
            assert stream is sys.stderr
        finally:
            # Restore original modules
            sys.modules.clear()
            sys.modules.update(original_modules)

    def test_get_foundation_log_stream_all_valid_options(self) -> None:
        """Test get_foundation_log_stream with all valid options."""
        # Test stderr
        assert get_foundation_log_stream("stderr") is sys.stderr

        # Test stdout
        assert get_foundation_log_stream("stdout") is sys.stdout

        # Test main (with mocked import)
        mock_stream = Mock()
        with patch.dict("sys.modules", {"provide.foundation.streams": Mock()}):
            mock_module = sys.modules["provide.foundation.streams"]
            mock_module.get_log_stream = Mock(return_value=mock_stream)
            assert get_foundation_log_stream("main") is mock_stream

    def test_get_foundation_log_stream_main_with_import_error_path(self) -> None:
        """Test get_foundation_log_stream main path specifically hitting ImportError handling."""
        # Ensure the module is not in sys.modules to force ImportError
        original_modules = sys.modules.copy()

        # Clear out potentially interfering modules
        for module_name in list(sys.modules.keys()):
            if "provide.foundation.streams" in module_name:
                del sys.modules[module_name]

        try:
            # This should trigger the ImportError path and call get_safe_stderr()
            stream = get_foundation_log_stream("main")
            assert stream is sys.stderr
        finally:
            sys.modules.clear()
            sys.modules.update(original_modules)

    def test_get_safe_stderr_edge_cases(self) -> None:
        """Test get_safe_stderr edge cases."""
        # Test when sys.stderr exists but is explicitly None
        original_stderr = getattr(sys, "stderr", None)
        try:
            sys.stderr = None
            stream = get_safe_stderr()
            assert isinstance(stream, io.StringIO)
        finally:
            sys.stderr = original_stderr

    def test_function_return_types(self) -> None:
        """Test that functions return the expected types."""
        stderr_stream = get_safe_stderr()
        assert hasattr(stderr_stream, "write")
        assert hasattr(stderr_stream, "flush")

        stdout_stream = get_foundation_log_stream("stdout")
        assert hasattr(stdout_stream, "write")
        assert hasattr(stdout_stream, "flush")


# 🧱🏗️🔚
