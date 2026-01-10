#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for provide.foundation.errors.types module."""

from __future__ import annotations

from datetime import datetime
import json

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

from provide.foundation.errors.types import (
    ErrorCode,
    ErrorMetadata,
    ErrorResponse,
)


class TestErrorCode(FoundationTestCase):
    """Test ErrorCode enum."""

    def test_config_error_codes(self) -> None:
        """Test configuration error codes."""
        assert ErrorCode.CONFIG_INVALID.value == "CFG_001"
        assert ErrorCode.CONFIG_MISSING.value == "CFG_002"
        assert ErrorCode.CONFIG_PARSE_ERROR.value == "CFG_003"
        assert ErrorCode.CONFIG_TYPE_ERROR.value == "CFG_004"

    def test_validation_error_codes(self) -> None:
        """Test validation error codes."""
        assert ErrorCode.VALIDATION_TYPE.value == "VAL_001"
        assert ErrorCode.VALIDATION_RANGE.value == "VAL_002"
        assert ErrorCode.VALIDATION_FORMAT.value == "VAL_003"
        assert ErrorCode.VALIDATION_REQUIRED.value == "VAL_004"
        assert ErrorCode.VALIDATION_CONSTRAINT.value == "VAL_005"

    def test_integration_error_codes(self) -> None:
        """Test integration error codes."""
        assert ErrorCode.INTEGRATION_TIMEOUT.value == "INT_001"
        assert ErrorCode.INTEGRATION_AUTH.value == "INT_002"
        assert ErrorCode.INTEGRATION_UNAVAILABLE.value == "INT_003"
        assert ErrorCode.INTEGRATION_RATE_LIMIT.value == "INT_004"
        assert ErrorCode.INTEGRATION_PROTOCOL.value == "INT_005"

    def test_resource_error_codes(self) -> None:
        """Test resource error codes."""
        assert ErrorCode.RESOURCE_NOT_FOUND.value == "RES_001"
        assert ErrorCode.RESOURCE_LOCKED.value == "RES_002"
        assert ErrorCode.RESOURCE_PERMISSION.value == "RES_003"
        assert ErrorCode.RESOURCE_EXHAUSTED.value == "RES_004"
        assert ErrorCode.RESOURCE_CONFLICT.value == "RES_005"

    def test_auth_error_codes(self) -> None:
        """Test authentication/authorization error codes."""
        assert ErrorCode.AUTH_INVALID_CREDENTIALS.value == "AUTH_001"
        assert ErrorCode.AUTH_TOKEN_EXPIRED.value == "AUTH_002"
        assert ErrorCode.AUTH_INSUFFICIENT_PERMISSION.value == "AUTH_003"
        assert ErrorCode.AUTH_SESSION_INVALID.value == "AUTH_004"
        assert ErrorCode.AUTH_MFA_REQUIRED.value == "AUTH_005"

    def test_system_error_codes(self) -> None:
        """Test system error codes."""
        assert ErrorCode.SYSTEM_UNAVAILABLE.value == "SYS_001"
        assert ErrorCode.SYSTEM_OVERLOAD.value == "SYS_002"
        assert ErrorCode.SYSTEM_MAINTENANCE.value == "SYS_003"
        assert ErrorCode.SYSTEM_INTERNAL.value == "SYS_004"
        assert ErrorCode.SYSTEM_PANIC.value == "SYS_005"

    def test_error_code_grouping(self) -> None:
        """Test that error codes are properly grouped by prefix."""
        # Config codes start with CFG
        assert all(code.value.startswith("CFG") for code in ErrorCode if "CONFIG" in code.name)

        # Validation codes start with VAL
        assert all(code.value.startswith("VAL") for code in ErrorCode if "VALIDATION" in code.name)


class TestErrorMetadata(FoundationTestCase):
    """Test ErrorMetadata class."""

    def test_default_creation(self) -> None:
        """Test creating ErrorMetadata with defaults."""
        meta = ErrorMetadata()

        assert meta.request_id is None
        assert meta.user_id is None
        assert meta.session_id is None
        assert meta.correlation_id is None
        assert meta.retry_count == 0
        assert meta.retry_after is None
        assert meta.help_url is None
        assert meta.support_id is None

    def test_creation_with_values(self) -> None:
        """Test creating ErrorMetadata with values."""
        meta = ErrorMetadata(
            request_id="req_123",
            user_id="user_456",
            session_id="sess_789",
            correlation_id="corr_012",
            retry_count=3,
            retry_after=5.0,
            help_url="https://example.com/help",
            support_id="sup_345",
        )

        assert meta.request_id == "req_123"
        assert meta.user_id == "user_456"
        assert meta.session_id == "sess_789"
        assert meta.correlation_id == "corr_012"
        assert meta.retry_count == 3
        assert meta.retry_after == 5.0
        assert meta.help_url == "https://example.com/help"
        assert meta.support_id == "sup_345"

    def test_to_dict_excludes_none(self) -> None:
        """Test that to_dict excludes None values."""
        meta = ErrorMetadata(request_id="req_123", retry_count=0)

        result = meta.to_dict()

        assert result == {"request_id": "req_123", "retry_count": 0}
        assert "user_id" not in result
        assert "session_id" not in result

    def test_to_dict_includes_non_none(self) -> None:
        """Test that to_dict includes all non-None values."""
        meta = ErrorMetadata(
            request_id="req_123",
            retry_count=0,
            retry_after=0.0,  # 0 is not None
        )

        result = meta.to_dict()

        assert result["retry_count"] == 0
        assert result["retry_after"] == 0.0


class TestErrorResponse(FoundationTestCase):
    """Test ErrorResponse class."""

    def test_creation_basic(self) -> None:
        """Test basic ErrorResponse creation."""
        response = ErrorResponse(
            error_code="TEST_001",
            message="Test error message",
        )

        assert response.error_code == "TEST_001"
        assert response.message == "Test error message"
        assert response.details is None
        assert response.metadata is None
        assert isinstance(response.timestamp, str)

    def test_creation_with_details(self) -> None:
        """Test ErrorResponse with details."""
        details = {"field": "email", "reason": "invalid format"}
        response = ErrorResponse(
            error_code="VAL_003",
            message="Email invalid",
            details=details,
        )

        assert response.details == details

    def test_creation_with_metadata(self) -> None:
        """Test ErrorResponse with metadata."""
        meta = ErrorMetadata(request_id="req_123", retry_count=2)
        response = ErrorResponse(error_code="INT_001", message="Timeout", metadata=meta)

        assert response.metadata is meta

    def test_timestamp_format(self) -> None:
        """Test that timestamp is ISO format."""
        with patch("provide.foundation.errors.types.datetime") as mock_dt:
            mock_now = datetime(2024, 1, 1, 12, 0, 0)
            mock_dt.now.return_value = mock_now

            response = ErrorResponse(error_code="TEST", message="Test")

            # The factory is called during class initialization
            # So we need to check the actual timestamp
            # It should be an ISO format string
            assert "T" in response.timestamp
            assert ":" in response.timestamp

    def test_to_dict_basic(self) -> None:
        """Test conversion to dictionary."""
        response = ErrorResponse(
            error_code="TEST_001",
            message="Test error",
            timestamp="2024-01-01T12:00:00",
        )

        result = response.to_dict()

        assert result == {
            "error_code": "TEST_001",
            "message": "Test error",
            "timestamp": "2024-01-01T12:00:00",
        }

    def test_to_dict_with_details(self) -> None:
        """Test to_dict with details."""
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            details={"key": "value"},
            timestamp="2024-01-01T12:00:00",
        )

        result = response.to_dict()

        assert result["details"] == {"key": "value"}

    def test_to_dict_with_metadata(self) -> None:
        """Test to_dict with metadata."""
        meta = ErrorMetadata(request_id="req_123", retry_count=1)
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            metadata=meta,
            timestamp="2024-01-01T12:00:00",
        )

        result = response.to_dict()

        assert result["metadata"] == {"request_id": "req_123", "retry_count": 1}

    def test_to_json(self) -> None:
        """Test JSON serialization."""
        response = ErrorResponse(
            error_code="TEST_001",
            message="Test error",
            details={"field": "value"},
            timestamp="2024-01-01T12:00:00",
        )

        json_str = response.to_json()
        parsed = json.loads(json_str)

        assert parsed["error_code"] == "TEST_001"
        assert parsed["message"] == "Test error"
        assert parsed["details"]["field"] == "value"
        assert parsed["timestamp"] == "2024-01-01T12:00:00"

    def test_to_json_formatting(self) -> None:
        """Test that JSON is properly formatted."""
        response = ErrorResponse(
            error_code="TEST",
            message="Error",
            timestamp="2024-01-01T12:00:00",
        )

        json_str = response.to_json()

        # Should be indented (2 spaces)
        assert "\n" in json_str
        assert "  " in json_str


# 🧱🏗️🔚
