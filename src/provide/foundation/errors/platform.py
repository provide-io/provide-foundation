#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Platform detection and system-related exceptions."""


class PlatformError(FoundationError):
    """Raised when platform detection or system operations fail.

    Args:
        message: Error message describing the platform issue.
        platform: Optional platform identifier.
        operation: Optional operation that failed.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise PlatformError("Failed to detect OS")
        >>> raise PlatformError("Unsupported platform", platform="freebsd")

    """

    def __init__(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "PLATFORM_ERROR"


# 🧱🏗️🔚
