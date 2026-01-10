#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for resource error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.resources import (
    AlreadyExistsError,
    NotFoundError,
    ResourceError,
)


class TestResourceError(FoundationTestCase):
    """Test ResourceError class."""

    def test_basic_creation(self) -> None:
        """Test basic ResourceError."""
        error = ResourceError("File not found")
        assert error.message == "File not found"
        assert error.code == "RESOURCE_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = ResourceError("Access denied", resource_type="file")
        assert error.context["resource.type"] == "file"

    def test_with_resource_path(self) -> None:
        """Test with resource_path parameter."""
        error = ResourceError("Not found", resource_path="/data/config.json")
        assert error.context["resource.path"] == "/data/config.json"


class TestNotFoundError(FoundationTestCase):
    """Test NotFoundError class."""

    def test_basic_creation(self) -> None:
        """Test basic NotFoundError."""
        error = NotFoundError("Resource not found")
        assert error.message == "Resource not found"
        assert error.code == "NOT_FOUND_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = NotFoundError("Not found", resource_type="user")
        assert error.context["notfound.type"] == "user"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = NotFoundError("Missing", resource_id="usr_123")
        assert error.context["notfound.id"] == "usr_123"


class TestAlreadyExistsError(FoundationTestCase):
    """Test AlreadyExistsError class."""

    def test_basic_creation(self) -> None:
        """Test basic AlreadyExistsError."""
        error = AlreadyExistsError("Already exists")
        assert error.message == "Already exists"
        assert error.code == "ALREADY_EXISTS_ERROR"

    def test_with_resource_type(self) -> None:
        """Test with resource_type parameter."""
        error = AlreadyExistsError("Duplicate", resource_type="email")
        assert error.context["exists.type"] == "email"

    def test_with_resource_id(self) -> None:
        """Test with resource_id parameter."""
        error = AlreadyExistsError("Conflict", resource_id="user@example.com")
        assert error.context["exists.id"] == "user@example.com"


# 🧱🏗️🔚
