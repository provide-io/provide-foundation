#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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

        # Avoid copying the dict unless we actually need to modify something.
        # Most log messages contain no secrets, so this saves an allocation
        # on every single log call.
        sanitized = None

        # Sanitize dictionary values (headers, config, etc.)
        if sanitize_dicts:
            for key, value in event_dict.items():
                if isinstance(value, dict):
                    new_value = sanitize_dict(value)
                    if new_value is not value:
                        if sanitized is None:
                            sanitized = event_dict.copy()
                        sanitized[key] = new_value

        # Mask secrets in string values
        if mask_patterns:
            source = sanitized if sanitized is not None else event_dict
            for key, value in source.items():
                if isinstance(value, str):
                    masked_value = mask_secrets(value)
                    if masked_value is not value:
                        if sanitized is None:
                            sanitized = event_dict.copy()
                        sanitized[key] = masked_value

        return sanitized if sanitized is not None else event_dict

    return sanitization_processor


__all__ = [
    "create_sanitization_processor",
]

# 🧱🏗️🔚
