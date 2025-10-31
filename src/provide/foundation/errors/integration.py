#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Integration and network-related exceptions."""


class IntegrationError(FoundationError):
    """Raised when external service integration fails.

    Args:
        message: Error message describing the integration failure.
        service: Optional service name that failed.
        endpoint: Optional endpoint that was called.
        status_code: Optional HTTP status code.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise IntegrationError("API call failed")
        >>> raise IntegrationError("Auth failed", service="github", status_code=401)

    """

    def __init__(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "INTEGRATION_ERROR"


class NetworkError(IntegrationError):
    """Raised for network-related failures.

    Args:
        message: Error message describing the network issue.
        host: Optional hostname or IP address.
        port: Optional port number.
        **kwargs: Additional context passed to IntegrationError.

    Examples:
        >>> raise NetworkError("Connection refused")
        >>> raise NetworkError("DNS resolution failed", host="api.example.com")

    """

    def __init__(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "NETWORK_ERROR"


class TimeoutError(IntegrationError):
    """Raised when operations exceed time limits.

    Args:
        message: Error message describing the timeout.
        timeout_seconds: Optional timeout limit in seconds.
        elapsed_seconds: Optional actual elapsed time.
        **kwargs: Additional context passed to IntegrationError.

    Examples:
        >>> raise TimeoutError("Request timed out")
        >>> raise TimeoutError("Operation exceeded limit", timeout_seconds=30, elapsed_seconds=31.5)

    """

    def __init__(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "TIMEOUT_ERROR"


# 🧱🏗️🔚
