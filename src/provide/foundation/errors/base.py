#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

"""Base exception class for Foundation."""


class FoundationError(Exception):
    """Base exception for all Foundation errors.

    Args:
        message: Human-readable error message.
        code: Optional error code for programmatic handling.
        context: Optional context dictionary with diagnostic data.
        cause: Optional underlying exception that caused this error.
        **extra_context: Additional key-value pairs added to context.

    Examples:
        >>> raise FoundationError("Operation failed")
        >>> raise FoundationError("Operation failed", code="OP_001")
        >>> raise FoundationError("Operation failed", user_id=123, retry_count=3)

    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def _default_code(self) -> str:
        """Return default error code for this exception type."""
        return "PROVIDE_ERROR"

    def add_context(self, key: str, value: Any) -> FoundationError:
        """Add context data to the error.

        Args:
            key: Context key (use dots for namespacing, e.g., 'aws.region').
            value: Context value.

        Returns:
            Self for method chaining.

        """
        self.context[key] = value
        return self

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result


# 🧱🏗️🔚
