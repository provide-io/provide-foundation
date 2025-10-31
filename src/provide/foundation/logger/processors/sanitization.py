#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

import structlog

from provide.foundation.security import mask_secrets, sanitize_dict

"""Security sanitization processor for logger.

Automatically sanitizes sensitive data from log messages using Foundation's
security utilities.
"""


def create_sanitization_processor(
    enabled: bool = True,
    mask_patterns: bool = True,
    sanitize_dicts: bool = True,
) -> Any:
    """Create a processor that sanitizes sensitive data from logs.

    This processor uses Foundation's security utilities to automatically:
    - Mask secrets based on common patterns (API keys, tokens, passwords)
    - Sanitize dictionary keys (Authorization, X-API-Key, etc.)

    Args:
        enabled: Whether sanitization is enabled
        mask_patterns: Whether to apply pattern-based secret masking
        sanitize_dicts: Whether to sanitize dictionary values

    Returns:
        Structlog processor function

    Examples:
        >>> log.info("API call", headers={"Authorization": "Bearer secret123"})
        # Logs: {"Authorization": "Bearer ***"}

        >>> log.info("Config loaded", api_key="sk-1234567890abcdef")
        # Logs: api_key="***"

    """

    def sanitization_processor(
        _logger: Any,
        _method_name: str,
        event_dict: structlog.types.EventDict,
    ) -> structlog.types.EventDict:
        """Apply sanitization to event dictionary."""
        if not enabled:
            return event_dict

        # Create a new dict to avoid modifying the original
        sanitized = event_dict.copy()

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in list(sanitized.items()):
                if isinstance(value, dict):
                    sanitized[key] = sanitize_dict(value)

        # Mask secrets in string values
        if mask_patterns:
            for key, value in list(sanitized.items()):
                if isinstance(value, str):
                    sanitized[key] = mask_secrets(value)

        return sanitized

    return sanitization_processor


__all__ = [
    "create_sanitization_processor",
]

# 🧱🏗️🔚
