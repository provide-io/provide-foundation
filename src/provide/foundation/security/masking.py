#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import re

from provide.foundation.security.defaults import DEFAULT_SECRET_PATTERNS, MASKED_VALUE

"""Secret masking utilities for command execution and sensitive strings."""


def mask_secrets(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def mask_command(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, secret_patterns, masked)


def should_mask(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in secret_patterns)


__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "MASKED_VALUE",
    "mask_command",
    "mask_secrets",
    "should_mask",
]

# 🧱🏗️🔚
