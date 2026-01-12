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
from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.handlers import (
    ErrorHandler,
    create_error_handler,
)
from provide.foundation.errors.integration import NetworkError


class TestErrorHandler(FoundationTestCase):
    """Test ErrorHandler class."""

    def test_default_creation(self) -> None:
        """Test creating ErrorHandler with defaults."""
        handler = ErrorHandler()

        assert handler.policies == {}
        assert handler.log_all is True
        assert handler.capture_context is True
        assert handler.reraise_unhandled is False

    def test_creation_with_policies(self) -> None:
        """Test creating ErrorHandler with policies."""

        def handle_value_error(e) -> str:
            return "handled"

        policies = {ValueError: handle_value_error}
        handler = ErrorHandler(policies=policies)

        assert handler.policies == policies

    def test_add_policy(self) -> None:
        """Test adding a policy."""
        handler = ErrorHandler()

        def handle_error(e) -> str:
            return "handled"

        result = handler.add_policy(ValueError, handle_error)

        assert result is handler  # Returns self
        assert handler.policies[ValueError] == handle_error

    def test_add_policy_chaining(self) -> None:
        """Test chaining policy additions."""
        handler = ErrorHandler()

        handler.add_policy(ValueError, lambda e: "val").add_policy(
            KeyError,
            lambda e: "key",
        )

        assert len(handler.policies) == 2

    def test_handle_with_matching_policy(self) -> None:
        """Test handling error with matching policy."""

        def handle_value(e) -> str:
            return f"handled: {e}"

        handler = ErrorHandler(policies={ValueError: handle_value})

        error = ValueError("test")
        result = handler.handle(error)

        assert result == "handled: test"

    def test_handle_with_default_action(self) -> None:
        """Test handling error with default action."""

        def default(e) -> str:
            return "default"

        handler = ErrorHandler(default_action=default)

        error = ValueError("test")
        result = handler.handle(error)

        assert result == "default"

    def test_handle_inheritance(self) -> None:
        """Test that policies match inherited error types."""

        def handle_foundation(e) -> str:
            return "foundation"

        handler = ErrorHandler(policies={FoundationError: handle_foundation})

        # ValidationError inherits from FoundationError
        error = ValidationError("test")
        result = handler.handle(error)

        assert result == "foundation"

    def test_reraise_unhandled(self) -> None:
        """Test that unhandled errors are reraised when configured."""
        handler = ErrorHandler(reraise_unhandled=True, default_action=lambda e: None)

        with pytest.raises(ValueError):
            handler.handle(ValueError("test"))

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_reraise_unhandled_logs_warning(self, mock_logger) -> None:
        """Test that reraising unhandled errors logs a warning."""
        handler = ErrorHandler(reraise_unhandled=True)

        with pytest.raises(ValueError):
            handler.handle(ValueError("test"))

        mock_logger.return_value.warning.assert_called()
        assert "No handler for ValueError" in mock_logger.return_value.warning.call_args[0][0]

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_enabled(self, mock_logger) -> None:
        """Test that handling is logged when log_all=True."""
        handler = ErrorHandler(policies={ValueError: lambda e: "handled"}, log_all=True)

        handler.handle(ValueError("test"))

        mock_logger.return_value.info.assert_called()
        assert "Handling ValueError" in mock_logger.return_value.info.call_args[0][0]

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_logging_disabled(self, mock_logger) -> None:
        """Test that handling is not logged when log_all=False."""
        handler = ErrorHandler(
            policies={ValueError: lambda e: "handled"},
            log_all=False,
        )

        handler.handle(ValueError("test"))

        mock_logger.return_value.info.assert_not_called()

    @patch("provide.foundation.errors.handlers.capture_error_context")
    def test_context_capture(self, mock_capture) -> None:
        """Test that context is captured when enabled."""
        mock_context = MagicMock()
        mock_context.to_dict.return_value = {}
        mock_capture.return_value = mock_context

        handler = ErrorHandler(capture_context=True)

        handler.handle(ValueError("test"))

        mock_capture.assert_called_once()

    def test_handler_exception_propagates(self) -> None:
        """Test that exceptions in handlers propagate."""

        def bad_handler(e) -> Never:
            raise RuntimeError("handler failed")

        handler = ErrorHandler(policies={ValueError: bad_handler})

        with pytest.raises(RuntimeError) as exc_info:
            handler.handle(ValueError("original"))

        assert str(exc_info.value) == "handler failed"
        assert exc_info.value.__cause__.args[0] == "original"

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_handler_exception_logged(self, mock_logger) -> None:
        """Test that handler exceptions are logged."""

        def bad_handler(e) -> Never:
            raise RuntimeError("handler failed")

        handler = ErrorHandler(policies={ValueError: bad_handler}, log_all=True)

        with pytest.raises(RuntimeError):
            handler.handle(ValueError("test"))

        # Should log both handling and failure
        assert mock_logger.return_value.info.call_count == 1
        assert mock_logger.return_value.error.call_count == 1
        assert "Error handler failed" in mock_logger.return_value.error.call_args[0][0]


class TestCreateErrorHandler(FoundationTestCase):
    """Test create_error_handler function."""

    def test_create_with_policies(self) -> None:
        """Test creating handler with policies."""
        handler = create_error_handler(
            ValidationError=lambda e: "validation",
            NetworkError=lambda e: "network",
        )

        assert ValidationError in handler.policies
        assert NetworkError in handler.policies

    def test_create_with_default(self) -> None:
        """Test creating handler with default action."""
        handler = create_error_handler(default=lambda e: "default_result")

        result = handler.handle(ValueError("test"))
        assert result == "default_result"

    def test_unknown_error_type_logged(self) -> None:
        """Test that unknown error types are logged."""
        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_logger:
            create_error_handler(NonExistentError=lambda e: "test")

            mock_logger.return_value.warning.assert_called()
            assert "Unknown error type: NonExistentError" in mock_logger.return_value.warning.call_args[0][0]

    def test_mixed_valid_and_invalid(self) -> None:
        """Test mixing valid and invalid error types."""
        with patch("provide.foundation.hub.foundation.get_foundation_logger"):
            handler = create_error_handler(
                ValidationError=lambda e: "valid",
                InvalidError=lambda e: "invalid",
                default=lambda e: "default",
            )

            # Valid error type should work
            assert handler.handle(ValidationError("test")) == "valid"

            # Invalid type falls back to default
            assert handler.handle(ValueError("test")) == "default"


# 🧱🏗️🔚
