#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import base64

from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveAuthenticationError,
)

"""Authentication handling for OpenObserve."""


def encode_basic_auth(username: str, password: str) -> str:
    """Encode username and password for Basic authentication.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Base64 encoded auth string

    """
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return encoded


def get_auth_headers(username: str | None, password: str | None) -> dict[str, str]:
    """Get authentication headers for OpenObserve API.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Dictionary with Authorization header

    Raises:
        OpenObserveAuthenticationError: If credentials are missing

    """
    if not username or not password:
        raise OpenObserveAuthenticationError(
            "OpenObserve credentials not configured. "
            "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
        )

    auth_token = encode_basic_auth(username, password)
    return {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }


def validate_credentials(username: str | None, password: str | None) -> tuple[str, str]:
    """Validate and return OpenObserve credentials.

    Args:
        username: OpenObserve username
        password: OpenObserve password

    Returns:
        Tuple of (username, password)

    Raises:
        OpenObserveAuthenticationError: If credentials are invalid

    """
    if not username:
        raise OpenObserveAuthenticationError("OpenObserve username is required")

    if not password:
        raise OpenObserveAuthenticationError("OpenObserve password is required")

    return username, password


# 🧱🏗️🔚
