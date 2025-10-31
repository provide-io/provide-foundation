#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Resource and filesystem-related exceptions."""


class ResourceError(FoundationError):
    """Raised when resource operations fail.

    Args:
        message: Error message describing the resource issue.
        resource_type: Optional type of resource (file, network, etc.).
        resource_path: Optional path or identifier of the resource.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ResourceError("File not found")
        >>> raise ResourceError("Permission denied", resource_type="file", resource_path="/etc/config")

    """

    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "RESOURCE_ERROR"


class NotFoundError(FoundationError):
    """Raised when a requested resource cannot be found.

    Args:
        message: Error message describing what was not found.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise NotFoundError("User not found")
        >>> raise NotFoundError("Entity missing", resource_type="user", resource_id="123")

    """

    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "NOT_FOUND_ERROR"


class AlreadyExistsError(FoundationError):
    """Raised when attempting to create a resource that already exists.

    Args:
        message: Error message describing the conflict.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AlreadyExistsError("User already registered")
        >>> raise AlreadyExistsError("Duplicate key", resource_type="user", resource_id="john@example.com")

    """

    def __init__(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "ALREADY_EXISTS_ERROR"


class LockError(FoundationError):
    """Raised when file lock operations fail.

    Args:
        message: Error message describing the lock issue.
        lock_path: Optional path to the lock file.
        timeout: Optional timeout that was exceeded.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise LockError("Failed to acquire lock")
        >>> raise LockError("Lock timeout", lock_path="/tmp/app.lock", timeout=30)

    """

    def __init__(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "LOCK_ERROR"


# 🧱🏗️🔚
