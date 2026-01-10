#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for runtime error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.runtime import ConcurrencyError, RuntimeError, StateError


class TestRuntimeError(FoundationTestCase):
    """Test RuntimeError class."""

    def test_basic_creation(self) -> None:
        """Test basic RuntimeError."""
        error = RuntimeError("Process failed")
        assert error.message == "Process failed"
        assert error.code == "RUNTIME_ERROR"
        assert error.context["runtime.retry_possible"] is False

    def test_with_operation(self) -> None:
        """Test with operation parameter."""
        error = RuntimeError("Lock failed", operation="acquire_lock")
        assert error.context["runtime.operation"] == "acquire_lock"

    def test_with_retry_possible(self) -> None:
        """Test with retry_possible parameter."""
        error = RuntimeError("Temporary failure", retry_possible=True)
        assert error.context["runtime.retry_possible"] is True


class TestStateError(FoundationTestCase):
    """Test StateError class."""

    def test_basic_creation(self) -> None:
        """Test basic StateError."""
        error = StateError("Invalid state")
        assert error.message == "Invalid state"
        assert error.code == "STATE_ERROR"

    def test_with_current_state(self) -> None:
        """Test with current_state parameter."""
        error = StateError("Cannot transition", current_state="pending")
        assert error.context["state.current"] == "pending"

    def test_with_expected_state(self) -> None:
        """Test with expected_state parameter."""
        error = StateError("Wrong state", expected_state="ready")
        assert error.context["state.expected"] == "ready"

    def test_with_transition(self) -> None:
        """Test with transition parameter."""
        error = StateError("Invalid", transition="start->running")
        assert error.context["state.transition"] == "start->running"


class TestConcurrencyError(FoundationTestCase):
    """Test ConcurrencyError class."""

    def test_basic_creation(self) -> None:
        """Test basic ConcurrencyError."""
        error = ConcurrencyError("Lock conflict")
        assert error.message == "Lock conflict"
        assert error.code == "CONCURRENCY_ERROR"

    def test_with_conflict_type(self) -> None:
        """Test with conflict_type parameter."""
        error = ConcurrencyError("Conflict", conflict_type="optimistic_lock")
        assert error.context["concurrency.type"] == "optimistic_lock"

    def test_with_version_expected(self) -> None:
        """Test with version_expected parameter."""
        error = ConcurrencyError("Version mismatch", version_expected=1)
        assert error.context["concurrency.version_expected"] == "1"

    def test_with_version_actual(self) -> None:
        """Test with version_actual parameter."""
        error = ConcurrencyError("Stale", version_actual=3)
        assert error.context["concurrency.version_actual"] == "3"

    def test_version_conversion(self) -> None:
        """Test that versions are converted to strings."""
        error = ConcurrencyError(
            "Version conflict",
            version_expected={"v": 1, "ts": 12345},
            version_actual={"v": 2, "ts": 12346},
        )
        assert "v" in error.context["concurrency.version_expected"]
        assert "v" in error.context["concurrency.version_actual"]


# 🧱🏗️🔚
