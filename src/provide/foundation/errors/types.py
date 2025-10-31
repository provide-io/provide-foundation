#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from attrs import define, field

from provide.foundation.serialization import json_dumps

"""Type definitions and constants for error handling.

Provides error codes, metadata structures, and retry policies.
"""


class ErrorCode(str, Enum):
    """Standard error codes for programmatic error handling.

    Use these codes for consistent error identification across the system.
    Codes are grouped by category with prefixes:
    - CFG: Configuration errors
    - VAL: Validation errors
    - INT: Integration errors
    - RES: Resource errors
    - AUTH: Authentication/Authorization errors
    - SYS: System errors
    """

    # Configuration errors (CFG)
    CONFIG_INVALID = "CFG_001"
    CONFIG_MISSING = "CFG_002"
    CONFIG_PARSE_ERROR = "CFG_003"
    CONFIG_TYPE_ERROR = "CFG_004"

    # Validation errors (VAL)
    VALIDATION_TYPE = "VAL_001"
    VALIDATION_RANGE = "VAL_002"
    VALIDATION_FORMAT = "VAL_003"
    VALIDATION_REQUIRED = "VAL_004"
    VALIDATION_CONSTRAINT = "VAL_005"

    # Integration errors (INT)
    INTEGRATION_TIMEOUT = "INT_001"
    INTEGRATION_AUTH = "INT_002"
    INTEGRATION_UNAVAILABLE = "INT_003"
    INTEGRATION_RATE_LIMIT = "INT_004"
    INTEGRATION_PROTOCOL = "INT_005"

    # Resource errors (RES)
    RESOURCE_NOT_FOUND = "RES_001"
    RESOURCE_LOCKED = "RES_002"
    RESOURCE_PERMISSION = "RES_003"
    RESOURCE_EXHAUSTED = "RES_004"
    RESOURCE_CONFLICT = "RES_005"

    # Authentication/Authorization errors (AUTH)
    AUTH_INVALID_CREDENTIALS = "AUTH_001"
    AUTH_TOKEN_EXPIRED = "AUTH_002"  # nosec B105 - This is an error code, not a password
    AUTH_INSUFFICIENT_PERMISSION = "AUTH_003"
    AUTH_SESSION_INVALID = "AUTH_004"
    AUTH_MFA_REQUIRED = "AUTH_005"

    # System errors (SYS)
    SYSTEM_UNAVAILABLE = "SYS_001"
    SYSTEM_OVERLOAD = "SYS_002"
    SYSTEM_MAINTENANCE = "SYS_003"
    SYSTEM_INTERNAL = "SYS_004"
    SYSTEM_PANIC = "SYS_005"


@define(kw_only=True, slots=True)
class ErrorMetadata:
    """Additional metadata for error tracking and debugging.

    Attributes:
        request_id: Optional request identifier for tracing.
        user_id: Optional user identifier.
        session_id: Optional session identifier.
        correlation_id: Optional correlation ID for distributed tracing.
        retry_count: Number of retry attempts made.
        retry_after: Seconds to wait before retry.
        help_url: Optional URL for more information.
        support_id: Optional support ticket/case ID.

    Examples:
        >>> meta = ErrorMetadata(
        ...     request_id="req_123",
        ...     user_id="user_456",
        ...     retry_count=2
        ... )

    """

    request_id: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    correlation_id: str | None = None
    retry_count: int = 0
    retry_after: float | None = None
    help_url: str | None = None
    support_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding None values.

        Returns:
            Dictionary with non-None metadata fields.

        """
        result = {}
        for key in [
            "request_id",
            "user_id",
            "session_id",
            "correlation_id",
            "retry_count",
            "retry_after",
            "help_url",
            "support_id",
        ]:
            value = getattr(self, key)
            if value is not None:
                result[key] = value
        return result


@define(kw_only=True, slots=True)
class ErrorResponse:
    """Structured error response for APIs and external interfaces.

    Attributes:
        error_code: Machine-readable error code.
        message: Human-readable error message.
        details: Optional additional error details.
        metadata: Optional error metadata.
        timestamp: When the error occurred.

    Examples:
        >>> response = ErrorResponse(
        ...     error_code="VAL_001",
        ...     message="Invalid email format",
        ...     details={"field": "email", "value": "not-an-email"}
        ... )

    """

    error_code: str
    message: str
    details: dict[str, Any] | None = None
    metadata: ErrorMetadata | None = None
    timestamp: str = field(factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of error response.

        """
        result: dict[str, Any] = {
            "error_code": self.error_code,
            "message": self.message,
            "timestamp": self.timestamp,
        }

        if self.details:
            result["details"] = self.details

        if self.metadata:
            result["metadata"] = self.metadata.to_dict()

        return result

    def to_json(self) -> str:
        """Convert to JSON string.

        Returns:
            JSON representation of error response.

        """
        return json_dumps(self.to_dict(), indent=2)


# Import datetime at module level for the factory

# 🧱🏗️🔚
