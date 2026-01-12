#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for authentication and authorization error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.auth import AuthenticationError, AuthorizationError


class TestAuthenticationError(FoundationTestCase):
    """Test AuthenticationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthenticationError."""
        error = AuthenticationError("Invalid credentials")
        assert error.message == "Invalid credentials"
        assert error.code == "AUTH_ERROR"

    def test_with_auth_method(self) -> None:
        """Test with auth_method parameter."""
        error = AuthenticationError("Token invalid", auth_method="jwt")
        assert error.context["auth.method"] == "jwt"

    def test_with_realm(self) -> None:
        """Test with realm parameter."""
        error = AuthenticationError("Access denied", realm="admin")
        assert error.context["auth.realm"] == "admin"


class TestAuthorizationError(FoundationTestCase):
    """Test AuthorizationError class."""

    def test_basic_creation(self) -> None:
        """Test basic AuthorizationError."""
        error = AuthorizationError("Permission denied")
        assert error.message == "Permission denied"
        assert error.code == "AUTHZ_ERROR"

    def test_with_required_permission(self) -> None:
        """Test with required_permission parameter."""
        error = AuthorizationError("Forbidden", required_permission="admin:write")
        assert error.context["authz.permission"] == "admin:write"

    def test_with_resource(self) -> None:
        """Test with resource parameter."""
        error = AuthorizationError("Cannot access", resource="/admin/users")
        assert error.context["authz.resource"] == "/admin/users"

    def test_with_actor(self) -> None:
        """Test with actor parameter."""
        error = AuthorizationError("Denied", actor="user:123")
        assert error.context["authz.actor"] == "user:123"


# 🧱🏗️🔚
