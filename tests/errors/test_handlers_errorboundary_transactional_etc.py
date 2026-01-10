#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for provide.foundation.errors.handlers module."""

from __future__ import annotations

from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.handlers import (
    error_boundary,
    handle_error,
    transactional,
)


class TestErrorBoundary(FoundationTestCase):
    """Test error_boundary context manager."""

    def test_no_error_passes_through(self) -> None:
        """Test that code without errors passes through."""
        with error_boundary(ValueError):
            result = 1 + 1

        assert result == 2

    def test_catches_specified_error(self) -> Never:
        """Test catching specified error type."""
        with error_boundary(ValueError, reraise=False):
            raise ValueError("test error")

        # Should not raise

    def test_catches_multiple_error_types(self) -> Never:
        """Test catching multiple error types."""
        with error_boundary(ValueError, KeyError, reraise=False):
            raise KeyError("test")

        # Should not raise

    def test_does_not_catch_unspecified_error(self) -> Never:
        """Test that unspecified errors are not caught."""
        with pytest.raises(TypeError), error_boundary(ValueError):
            raise TypeError("not caught")

    def test_reraise_true_reraises(self) -> Never:
        """Test that reraise=True reraises the error."""
        with pytest.raises(ValueError), error_boundary(ValueError, reraise=True):
            raise ValueError("test")

    def test_fallback_value_when_not_reraising(self) -> Never:
        """Test fallback value is available when not reraising."""
        # error_boundary returns fallback when reraise=False
        with error_boundary(ValueError, reraise=False, fallback="default"):
            raise ValueError("test")

        # The context manager itself doesn't return the fallback
        # It's used internally

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_enabled(self, mock_logger) -> Never:
        """Test that errors are logged when log_errors=True."""
        with error_boundary(ValueError, log_errors=True, reraise=False):
            raise ValueError("test error")

        mock_logger.return_value.error.assert_called_once()
        call_args = mock_logger.return_value.error.call_args
        assert "Error caught in boundary" in call_args[0][0]
        assert call_args[1]["error.type"] == "ValueError"
        assert call_args[1]["error.message"] == "test error"

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_disabled(self, mock_logger) -> Never:
        """Test that errors are not logged when log_errors=False."""
        with error_boundary(ValueError, log_errors=False, reraise=False):
            raise ValueError("test")

        mock_logger.return_value.error.assert_not_called()

    def test_context_added_to_logs(self) -> Never:
        """Test that provided context is added to logs."""
        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_logger:
            context = {"request_id": "123", "user": "test"}

            with error_boundary(
                ValueError,
                log_errors=True,
                reraise=False,
                context=context,
            ):
                raise ValueError("test")

            call_args = mock_logger.return_value.error.call_args[1]
            assert call_args["request_id"] == "123"
            assert call_args["user"] == "test"

    def test_foundation_error_context_merged(self) -> Never:
        """Test that FoundationError context is merged."""
        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_logger:
            error = FoundationError("test", user_id=456)

            with error_boundary(FoundationError, log_errors=True, reraise=False):
                raise error

            call_args = mock_logger.return_value.error.call_args[1]
            assert call_args["user_id"] == 456

    def test_on_error_callback(self) -> Never:
        """Test that on_error callback is called."""
        callback = MagicMock()

        with error_boundary(ValueError, on_error=callback, reraise=False):
            raise ValueError("test")

        callback.assert_called_once()
        assert isinstance(callback.call_args[0][0], ValueError)

    def test_on_error_callback_exception_logged(self) -> Never:
        """Test that exceptions in on_error are logged."""

        def bad_callback(e) -> Never:
            raise RuntimeError("callback failed")

        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_logger:
            with error_boundary(
                ValueError,
                on_error=bad_callback,
                log_errors=True,
                reraise=False,
            ):
                raise ValueError("test")

            # Should log both the original error and callback error
            assert mock_logger.return_value.error.call_count == 2
            assert "callback failed" in str(
                mock_logger.return_value.error.call_args_list[1],
            )

    def test_default_catches_all_exceptions(self) -> Never:
        """Test that empty catch list defaults to Exception."""
        with error_boundary(reraise=False):
            raise RuntimeError("any error")

        # Should not raise


class TestTransactional(FoundationTestCase):
    """Test transactional context manager."""

    def test_commit_on_success(self) -> None:
        """Test that commit is called on success."""
        rollback = MagicMock()
        commit = MagicMock()

        with transactional(rollback, commit):
            result = 1 + 1

        commit.assert_called_once()
        rollback.assert_not_called()
        assert result == 2

    def test_rollback_on_error(self) -> Never:
        """Test that rollback is called on error."""
        rollback = MagicMock()
        commit = MagicMock()

        with pytest.raises(ValueError), transactional(rollback, commit):
            raise ValueError("test")

        rollback.assert_called_once()
        commit.assert_not_called()

    def test_no_commit_function(self) -> None:
        """Test that commit is optional."""
        rollback = MagicMock()

        with transactional(rollback):
            pass

        rollback.assert_not_called()

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_error_logged(self, mock_logger) -> Never:
        """Test that errors are logged."""
        rollback = MagicMock()

        with pytest.raises(ValueError), transactional(rollback, log_errors=True):
            raise ValueError("test error")

        mock_logger.return_value.error.assert_called()
        assert "Transaction failed" in mock_logger.return_value.error.call_args[0][0]

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_successful_rollback_logged(self, mock_logger) -> Never:
        """Test that successful rollback is logged."""
        rollback = MagicMock()

        with pytest.raises(ValueError), transactional(rollback, log_errors=True):
            raise ValueError("test")

        mock_logger.return_value.info.assert_called_with(
            "Transaction rolled back successfully",
        )

    def test_rollback_failure_raises_rollback_error(self) -> Never:
        """Test that rollback failure raises the rollback error."""

        def failing_rollback() -> Never:
            raise RuntimeError("rollback failed")

        with pytest.raises(RuntimeError) as exc_info, transactional(failing_rollback):
            raise ValueError("original error")

        assert str(exc_info.value) == "rollback failed"
        assert exc_info.value.__cause__.args[0] == "original error"

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_rollback_failure_logged_as_critical(self, mock_logger) -> Never:
        """Test that rollback failure is logged as critical."""

        def failing_rollback() -> Never:
            raise RuntimeError("rollback failed")

        with pytest.raises(RuntimeError), transactional(failing_rollback, log_errors=True):
            raise ValueError("original")

        mock_logger.return_value.critical.assert_called()
        assert "Rollback failed" in mock_logger.return_value.critical.call_args[0][0]

    def test_on_error_callback(self) -> Never:
        """Test that on_error callback is called."""
        rollback = MagicMock()
        on_error = MagicMock()

        with pytest.raises(ValueError), transactional(rollback, on_error=on_error):
            raise ValueError("test")

        on_error.assert_called_once()
        assert isinstance(on_error.call_args[0][0], ValueError)

    def test_on_error_exception_handled(self) -> Never:
        """Test that exceptions in on_error don't prevent rollback."""
        rollback = MagicMock()

        def bad_handler(e) -> Never:
            raise RuntimeError("handler failed")

        with pytest.raises(ValueError), transactional(rollback, on_error=bad_handler):
            raise ValueError("original")

        # Rollback should still be called
        rollback.assert_called_once()


class TestHandleError(FoundationTestCase):
    """Test handle_error function."""

    def test_basic_error_handling(self) -> None:
        """Test basic error handling."""
        error = ValueError("test")
        result = handle_error(error, fallback="default")

        assert result == "default"

    def test_reraise_error(self) -> None:
        """Test that reraise=True raises the error."""
        error = ValueError("test")

        with pytest.raises(ValueError):
            handle_error(error, reraise=True)

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_enabled(self, mock_logger) -> None:
        """Test that error is logged when log=True."""
        error = ValueError("test error")

        handle_error(error, log=True)

        mock_logger.return_value.error.assert_called_once()
        assert "Handling error" in mock_logger.return_value.error.call_args[0][0]

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_disabled(self, mock_logger) -> None:
        """Test that error is not logged when log=False."""
        error = ValueError("test")

        handle_error(error, log=False)

        mock_logger.return_value.error.assert_not_called()

    @patch("provide.foundation.errors.handlers.capture_error_context")
    def test_context_capture(self, mock_capture) -> None:
        """Test that error context is captured."""
        mock_context = MagicMock()
        mock_context.to_dict.return_value = {"test": "context"}
        mock_capture.return_value = mock_context

        error = ValueError("test")

        handle_error(error, capture_context=True)

        mock_capture.assert_called_once_with(error)

    @patch("provide.foundation.errors.handlers.capture_error_context")
    def test_context_not_captured(self, mock_capture) -> None:
        """Test that context is not captured when disabled."""
        error = ValueError("test")

        handle_error(error, capture_context=False)

        mock_capture.assert_not_called()

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    @patch("provide.foundation.errors.handlers.capture_error_context")
    def test_context_added_to_logs(self, mock_capture, mock_logger) -> None:
        """Test that captured context is added to logs."""
        mock_context = MagicMock()
        mock_context.to_dict.return_value = {"captured": "data"}
        mock_capture.return_value = mock_context

        error = ValueError("test")

        handle_error(error, log=True, capture_context=True)

        call_args = mock_logger.return_value.error.call_args[1]
        assert call_args["captured"] == "data"


# 🧱🏗️🔚
