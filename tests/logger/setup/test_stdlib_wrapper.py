#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import logging

from provide.testkit.mocking import MagicMock

from provide.foundation.logger.setup.stdlib_wrapper import StructuredStdlibLogger


class TestStructuredStdlibLogger:
    """Test the StructuredStdlibLogger wrapper."""

    def test_wrapper_accepts_kwargs(self) -> None:
        """Test that the wrapper accepts structlog-style kwargs."""
        mock_logger = MagicMock(spec=logging.Logger)
        wrapper = StructuredStdlibLogger(mock_logger)

        wrapper.debug("Test message", key1="value1", key2="value2")

        # Verify the underlying logger was called with extra dict
        mock_logger.log.assert_called_once()
        args, kwargs = mock_logger.log.call_args
        assert args[0] == logging.DEBUG
        assert args[1] == "Test message"
        assert "extra" in kwargs
        assert kwargs["extra"]["key1"] == "value1"
        assert kwargs["extra"]["key2"] == "value2"

    def test_wrapper_preserves_stdlib_kwargs(self) -> None:
        """Test that stdlib logging kwargs are preserved."""
        mock_logger = MagicMock(spec=logging.Logger)
        wrapper = StructuredStdlibLogger(mock_logger)

        exc = Exception("test error")
        wrapper.error("Error occurred", exc_info=exc, stack_info=True, custom_key="value")

        _args, kwargs = mock_logger.log.call_args
        assert "exc_info" in kwargs
        assert kwargs["exc_info"] == exc
        assert "stack_info" in kwargs
        assert kwargs["stack_info"] is True
        assert "extra" in kwargs
        assert kwargs["extra"]["custom_key"] == "value"

    def test_wrapper_merges_extra_dicts(self) -> None:
        """Test that existing extra dict is merged with new kwargs."""
        mock_logger = MagicMock(spec=logging.Logger)
        wrapper = StructuredStdlibLogger(mock_logger)

        existing_extra = {"existing": "value"}
        wrapper.info("Test", extra=existing_extra, new_key="new_value")

        _args, kwargs = mock_logger.log.call_args
        assert "extra" in kwargs
        assert kwargs["extra"]["existing"] == "value"
        assert kwargs["extra"]["new_key"] == "new_value"

    def test_all_log_levels(self) -> None:
        """Test all log level methods work."""
        mock_logger = MagicMock(spec=logging.Logger)
        wrapper = StructuredStdlibLogger(mock_logger)

        wrapper.debug("Debug message", key="debug")
        wrapper.info("Info message", key="info")
        wrapper.warning("Warning message", key="warning")
        wrapper.error("Error message", key="error")
        wrapper.critical("Critical message", key="critical")

        assert mock_logger.log.call_count == 5

        # Check the log levels were correct
        calls = mock_logger.log.call_args_list
        assert calls[0][0][0] == logging.DEBUG
        assert calls[1][0][0] == logging.INFO
        assert calls[2][0][0] == logging.WARNING
        assert calls[3][0][0] == logging.ERROR
        assert calls[4][0][0] == logging.CRITICAL


# 🧱🏗️🔚
