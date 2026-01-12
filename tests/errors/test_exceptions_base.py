#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for provide.foundation.errors.exceptions module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.base import FoundationError


class TestFoundationError(FoundationTestCase):
    """Test the base FoundationError class."""

    def test_basic_creation(self) -> None:
        """Test basic error creation."""
        error = FoundationError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "PROVIDE_ERROR"
        assert error.context == {}
        assert error.cause is None

    def test_with_code(self) -> None:
        """Test error with custom code."""
        error = FoundationError("Test error", code="CUSTOM_001")
        assert error.code == "CUSTOM_001"

    def test_with_context(self) -> None:
        """Test error with initial context."""
        context = {"key": "value", "number": 42}
        error = FoundationError("Test error", context=context)
        assert error.context == context

    def test_with_cause(self) -> None:
        """Test error with cause."""
        cause = ValueError("Original error")
        error = FoundationError("Wrapped error", cause=cause)
        assert error.cause is cause
        assert error.__cause__ is cause

    def test_with_extra_context(self) -> None:
        """Test error with extra context via kwargs."""
        error = FoundationError(
            "Test error",
            user_id=123,
            request_id="req_456",
            retry_count=3,
        )
        assert error.context == {
            "user_id": 123,
            "request_id": "req_456",
            "retry_count": 3,
        }

    def test_context_merge(self) -> None:
        """Test that extra context merges with provided context."""
        error = FoundationError(
            "Test error",
            context={"existing": "value"},
            new_key="new_value",
            number=42,
        )
        assert error.context == {
            "existing": "value",
            "new_key": "new_value",
            "number": 42,
        }

    def test_add_context(self) -> None:
        """Test adding context after creation."""
        error = FoundationError("Test error")
        error.add_context("key1", "value1")
        error.add_context("key2", 42)

        assert error.context == {"key1": "value1", "key2": 42}

    def test_add_context_chaining(self) -> None:
        """Test that add_context returns self for chaining."""
        error = FoundationError("Test error")
        result = error.add_context("key1", "value1").add_context("key2", "value2")

        assert result is error
        assert error.context == {"key1": "value1", "key2": "value2"}

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        cause = ValueError("Original")
        error = FoundationError(
            "Test error",
            code="TEST_001",
            context={"user_id": 123},
            cause=cause,
            request_id="req_456",
        )

        result = error.to_dict()

        assert result["error.type"] == "FoundationError"
        assert result["error.message"] == "Test error"
        assert result["error.code"] == "TEST_001"
        assert result["error.user_id"] == 123
        assert result["error.request_id"] == "req_456"
        assert result["error.cause"] == "Original"
        assert result["error.cause_type"] == "ValueError"

    def test_to_dict_with_namespaced_context(self) -> None:
        """Test that namespaced context keys are preserved."""
        error = FoundationError("Test error")
        error.add_context("aws.region", "us-east-1")
        error.add_context("http.status", 500)
        error.add_context("simple_key", "value")

        result = error.to_dict()

        assert result["aws.region"] == "us-east-1"
        assert result["http.status"] == 500
        assert result["error.simple_key"] == "value"

    def test_default_code_override(self) -> None:
        """Test that subclasses can override default code."""

        class CustomError(FoundationError):
            def _default_code(self) -> str:
                return "CUSTOM_ERROR"

        error = CustomError("Test")
        assert error.code == "CUSTOM_ERROR"

        # Can still override with explicit code
        error2 = CustomError("Test", code="OVERRIDE")
        assert error2.code == "OVERRIDE"


# 🧱🏗️🔚
