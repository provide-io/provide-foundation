#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import re

from provide.foundation.security.defaults import DEFAULT_SECRET_PATTERNS, MASKED_VALUE

"""Secret masking utilities for command execution and sensitive strings."""

# Pre-compile default patterns at module load time for performance.
# This avoids re-compiling 22 regex patterns on every log message.
_COMPILED_DEFAULT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(pattern, re.IGNORECASE) for pattern in DEFAULT_SECRET_PATTERNS
]

# Fast-path keywords: if none of these substrings appear (case-insensitive),
# the text cannot match any DEFAULT_SECRET_PATTERNS. This lets us skip all
# 22 regex scans on the vast majority of log messages.
#
# Note: bare "key" was replaced with targeted variants to avoid false
# positives on common strings like "key_value". The patterns that use
# "key" all require context: api_key, access_key, secret_key (covered
# by "api", "access", "secret"), or [A-Z_]+KEY= (covered by "key=", "key:").
_DEFAULT_QUICK_CHECK_KEYWORDS: tuple[str, ...] = (
    "password",
    "passwd",
    "pwd",
    "token",
    "secret",
    "auth",
    "credential",
    "-p ",
    "api",  # covers api_key, api-key, apikey, api_token, api-token
    "access",  # covers access_key, access-key
    "key=",  # covers [A-Z_]+KEY= env var patterns (after lowering)
    "key:",  # covers [A-Z_]+KEY: env var patterns (after lowering)
)

# Cache for custom pattern compilations
_compiled_pattern_cache: dict[tuple[str, ...], list[re.Pattern[str]]] = {}


def _get_compiled_patterns(secret_patterns: list[str] | None) -> list[re.Pattern[str]]:
    """Get compiled regex patterns, using cache for repeated calls."""
    if secret_patterns is None:
        return _COMPILED_DEFAULT_PATTERNS

    key = tuple(secret_patterns)
    compiled = _compiled_pattern_cache.get(key)
    if compiled is not None:
        return compiled

    compiled = [re.compile(p, re.IGNORECASE) for p in secret_patterns]
    _compiled_pattern_cache[key] = compiled
    return compiled


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
    # Fast path: for default patterns, do a cheap case-insensitive keyword
    # check before running any regex. Most log messages contain no secret
    # keywords, so this skips all 22 pattern.sub() calls.
    if secret_patterns is None:
        text_lower = text.lower()
        if not any(kw in text_lower for kw in _DEFAULT_QUICK_CHECK_KEYWORDS):
            return text

    compiled = _get_compiled_patterns(secret_patterns)

    result = text
    for pattern in compiled:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = pattern.sub(
            lambda m: f"{m.group(1)}{masked}",
            result,
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
    # Fast path: no keywords means no secrets possible
    if secret_patterns is None:
        text_lower = text.lower()
        if not any(kw in text_lower for kw in _DEFAULT_QUICK_CHECK_KEYWORDS):
            return False

    compiled = _get_compiled_patterns(secret_patterns)
    return any(pattern.search(text) for pattern in compiled)


__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "MASKED_VALUE",
    "mask_command",
    "mask_secrets",
    "should_mask",
]

# 🧱🏗️🔚
