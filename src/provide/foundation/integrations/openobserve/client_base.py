#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Base OpenObserve client with core functionality."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.auth import (
    get_auth_headers,
    validate_credentials,
)
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveQueryError,
)
from provide.foundation.logger import get_logger
from provide.foundation.transport import UniversalClient
from provide.foundation.transport.errors import (
    TransportConnectionError,
    TransportError,
    TransportTimeoutError,
)

log = get_logger(__name__)


class OpenObserveClientBase:
    """Base OpenObserve client with core HTTP functionality.

    Uses Foundation's transport system for all HTTP operations.
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    @classmethod
    def from_config(cls) -> OpenObserveClientBase:
        """Create client from OpenObserveConfig.

        Returns:
            Configured OpenObserveClient instance

        Raises:
            OpenObserveConfigError: If configuration is missing

        """
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig

        config = OpenObserveConfig.from_env()

        if not config.url:
            raise OpenObserveConfigError(
                "OpenObserve URL not configured. Set OPENOBSERVE_URL environment variable.",
            )

        if not config.user or not config.password:
            raise OpenObserveConfigError(
                "OpenObserve credentials not configured. "
                "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
            )

        return cls(
            url=config.url,
            username=config.user,
            password=config.password,
            organization=config.org or "default",
        )

    def _extract_error_message(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def _check_response_errors(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e


# 🧱🏗️🔚
