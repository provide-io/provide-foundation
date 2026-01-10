#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve client error handling.

This module tests error message extraction, response error checking, and exception handling.
Run with: pytest tests/integrations/openobserve/test_client_error_handling.py -v"""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConnectionError,
    OpenObserveQueryError,
)


class MockResponse:
    """Mock response object for testing."""

    def __init__(
        self,
        status: int = 200,
        body: bytes | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.body = body or b"{}"
        self._json_data = json_data or {}

    def is_success(self) -> bool:
        """Check if response is successful."""
        return 200 <= self.status < 300

    def json(self) -> dict[str, Any]:
        """Return JSON data."""
        return self._json_data


class TestExtractErrorMessage(FoundationTestCase):
    """Tests for _extract_error_message method."""

    def test_extract_error_message_from_json(self) -> None:
        """Test extracting error message from JSON response."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(
            status=400,
            json_data={"message": "Invalid query syntax"},
        )

        error_msg = client._extract_error_message(response, "Default error")

        assert error_msg == "Invalid query syntax"

    def test_extract_error_message_default(self) -> None:
        """Test using default message when extraction fails."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(status=500, json_data={})

        error_msg = client._extract_error_message(response, "Default error")

        assert error_msg == "Default error"

    def test_extract_error_message_invalid_json(self) -> None:
        """Test handling invalid JSON in response."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        # Mock response with invalid JSON
        response = MagicMock()
        response.json.side_effect = ValueError("Invalid JSON")

        error_msg = client._extract_error_message(response, "Default error")

        assert error_msg == "Default error"


class TestCheckResponseErrors(FoundationTestCase):
    """Tests for _check_response_errors method."""

    def test_check_response_401_raises_connection_error(self) -> None:
        """Test that 401 raises OpenObserveConnectionError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(status=401)

        with pytest.raises(OpenObserveConnectionError, match="Authentication failed"):
            client._check_response_errors(response)

    def test_check_response_400_raises_query_error(self) -> None:
        """Test that 400 raises OpenObserveQueryError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(
            status=400,
            json_data={"message": "Bad request"},
        )

        with pytest.raises(OpenObserveQueryError, match="Bad request"):
            client._check_response_errors(response)

    def test_check_response_500_raises_query_error(self) -> None:
        """Test that 500 raises OpenObserveQueryError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(status=500)

        with pytest.raises(OpenObserveQueryError, match="HTTP 500 error"):
            client._check_response_errors(response)

    def test_check_response_success_no_error(self) -> None:
        """Test that successful responses don't raise errors."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        response = MockResponse(status=200)

        # Should not raise
        client._check_response_errors(response)


__all__ = [
    "TestCheckResponseErrors",
    "TestExtractErrorMessage",
]

# 🧱🏗️🔚
