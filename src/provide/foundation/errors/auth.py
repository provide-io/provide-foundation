#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Authentication and authorization exceptions."""


class AuthenticationError(FoundationError):
    """Raised when authentication fails.

    Args:
        message: Error message describing the authentication failure.
        auth_method: Optional authentication method used.
        realm: Optional authentication realm.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AuthenticationError("Invalid credentials")
        >>> raise AuthenticationError("Token expired", auth_method="jwt")

    """

    def __init__(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "AUTH_ERROR"


class AuthorizationError(FoundationError):
    """Raised when authorization fails.

    Args:
        message: Error message describing the authorization failure.
        required_permission: Optional required permission.
        resource: Optional resource being accessed.
        actor: Optional actor (user/service) attempting access.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AuthorizationError("Access denied")
        >>> raise AuthorizationError("Insufficient permissions", required_permission="admin")

    """

    def __init__(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "AUTHZ_ERROR"


# 🧱🏗️🔚
