#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from provide.foundation.security.defaults import (
    DEFAULT_SENSITIVE_HEADERS,
    DEFAULT_SENSITIVE_PARAMS,
    REDACTED_VALUE,
)

"""Sanitization utilities for sensitive data redaction in logs and outputs."""


def sanitize_headers(
    headers: Mapping[str, Any],
    sensitive_headers: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> dict[str, Any]:
    """Sanitize sensitive headers for safe logging.

    Args:
        headers: Headers dictionary to sanitize
        sensitive_headers: List of header names to redact (case-insensitive)
        redacted: Replacement value for redacted headers

    Returns:
        Sanitized headers dictionary

    """
    if sensitive_headers is None:
        sensitive_headers = DEFAULT_SENSITIVE_HEADERS

    # Convert sensitive headers to lowercase for case-insensitive matching
    sensitive_lower = {h.lower() for h in sensitive_headers}

    sanitized = {}
    for key, value in headers.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        else:
            sanitized[key] = value

    return sanitized


def sanitize_uri(
    uri: str,
    sensitive_params: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
) -> str:
    """Sanitize sensitive query parameters in URI for safe logging.

    Args:
        uri: URI to sanitize
        sensitive_params: List of parameter names to redact (case-insensitive)
        redacted: Replacement value for redacted parameters

    Returns:
        Sanitized URI string

    """
    if sensitive_params is None:
        sensitive_params = DEFAULT_SENSITIVE_PARAMS

    # Parse URI
    parsed = urlparse(uri)

    # If no query string, return as-is
    if not parsed.query:
        return uri

    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)

    # Convert sensitive params to lowercase for case-insensitive matching
    sensitive_lower = {p.lower() for p in sensitive_params}

    # Sanitize sensitive parameters
    sanitized_params = {}
    for key, values in params.items():
        if key.lower() in sensitive_lower:
            # Redact all values for this parameter
            sanitized_params[key] = [redacted] * len(values)
        else:
            sanitized_params[key] = values

    # Rebuild query string
    new_query = urlencode(sanitized_params, doseq=True)

    # Rebuild URI
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def sanitize_dict(
    data: dict[str, Any],
    sensitive_keys: list[str] | None = None,
    redacted: str = REDACTED_VALUE,
    recursive: bool = True,
) -> dict[str, Any]:
    """Sanitize sensitive keys in dictionary for safe logging.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys to redact (case-insensitive)
        redacted: Replacement value for redacted values
        recursive: Whether to recursively sanitize nested dicts

    Returns:
        Sanitized dictionary

    """
    if sensitive_keys is None:
        # Use combined list of headers and params as defaults
        sensitive_keys = DEFAULT_SENSITIVE_HEADERS + DEFAULT_SENSITIVE_PARAMS

    # Convert sensitive keys to lowercase for case-insensitive matching
    sensitive_lower = {k.lower() for k in sensitive_keys}

    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in sensitive_lower:
            sanitized[key] = redacted
        elif recursive and isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys, redacted, recursive)
        elif recursive and isinstance(value, list):
            # Sanitize list elements if they're dicts
            sanitized[key] = [
                sanitize_dict(item, sensitive_keys, redacted, recursive) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def should_sanitize_body(content_type: str | None) -> bool:
    """Determine if body should be sanitized based on content type.

    Args:
        content_type: Content-Type header value

    Returns:
        True if body should be sanitized

    """
    if not content_type:
        return False

    # Sanitize JSON and form data, skip binary formats
    content_type_lower = content_type.lower()
    return any(
        ct in content_type_lower
        for ct in [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        ]
    )


__all__ = [
    "DEFAULT_SENSITIVE_HEADERS",
    "DEFAULT_SENSITIVE_PARAMS",
    "REDACTED_VALUE",
    "sanitize_dict",
    "sanitize_headers",
    "sanitize_uri",
    "should_sanitize_body",
]

# 🧱🏗️🔚
