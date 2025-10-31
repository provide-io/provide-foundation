#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Runtime and process execution exceptions."""


class RuntimeError(FoundationError):
    """Raised for runtime operational errors.

    Args:
        message: Error message describing the runtime issue.
        operation: Optional operation that failed.
        retry_possible: Whether the operation can be retried.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise RuntimeError("Process failed")
        >>> raise RuntimeError("Lock timeout", operation="acquire_lock", retry_possible=True)

    """

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "RUNTIME_ERROR"


class StateError(FoundationError):
    """Raised when an operation is invalid for the current state.

    Args:
        message: Error message describing the state issue.
        current_state: Optional current state.
        expected_state: Optional expected state.
        transition: Optional attempted transition.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise StateError("Invalid state transition")
        >>> raise StateError("Not ready", current_state="initializing", expected_state="ready")

    """

    def __init__(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "STATE_ERROR"


class ConcurrencyError(FoundationError):
    """Raised when concurrency conflicts occur.

    Args:
        message: Error message describing the concurrency issue.
        conflict_type: Optional type of conflict (lock, version, etc.).
        version_expected: Optional expected version.
        version_actual: Optional actual version.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ConcurrencyError("Optimistic lock failure")
        >>> raise ConcurrencyError("Version mismatch", version_expected=1, version_actual=2)

    """

    def __init__(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "CONCURRENCY_ERROR"


class RateLimitExceededError(FoundationError):
    """Raised when a rate limit is exceeded.

    Args:
        message: Error message describing the rate limit violation.
        limit: The rate limit that was exceeded (requests/messages per time unit).
        retry_after: Seconds to wait before retrying.
        current_rate: Optional current rate at time of error.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise RateLimitExceededError("Log rate limit exceeded", limit=100.0, retry_after=1.0)
        >>> raise RateLimitExceededError("API rate limit", limit=1000, retry_after=60, current_rate=1050)

    """

    def __init__(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "INTEGRATION_RATE_LIMIT"


# 🧱🏗️🔚
