from __future__ import annotations

import re

"""Secret masking utilities for command execution and sensitive strings."""

# Default secret patterns (case-insensitive regex patterns)
DEFAULT_SECRET_PATTERNS = [
    # Key-value patterns (key=value, key:value, key value)
    r"(password[=:\s]+)([^\s]+)",
    r"(passwd[=:\s]+)([^\s]+)",
    r"(pwd[=:\s]+)([^\s]+)",
    r"(token[=:\s]+)([^\s]+)",
    r"(api[_-]?key[=:\s]+)([^\s]+)",
    r"(api[_-]?token[=:\s]+)([^\s]+)",
    r"(access[_-]?key[=:\s]+)([^\s]+)",
    r"(secret[_-]?key[=:\s]+)([^\s]+)",
    r"(secret[=:\s]+)([^\s]+)",
    r"(auth[=:\s]+)([^\s]+)",
    r"(credentials?[=:\s]+)([^\s]+)",
    # CLI flag patterns (--flag value, --flag=value, -f value)
    r"(--password[=\s]+)([^\s]+)",
    r"(--token[=\s]+)([^\s]+)",
    r"(--api-key[=\s]+)([^\s]+)",
    r"(--api-token[=\s]+)([^\s]+)",
    r"(--secret[=\s]+)([^\s]+)",
    r"(--auth[=\s]+)([^\s]+)",
    r"(-p\s+)([^\s]+)",  # Common -p flag for password
    # Environment variable patterns
    r"([A-Z_]+PASSWORD[=:])([^\s]+)",
    r"([A-Z_]+TOKEN[=:])([^\s]+)",
    r"([A-Z_]+KEY[=:])([^\s]+)",
    r"([A-Z_]+SECRET[=:])([^\s]+)",
]

# Masked placeholder
MASKED_VALUE = "[MASKED]"


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
    if isinstance(cmd, list):
        cmd_str = " ".join(cmd)
    else:
        cmd_str = cmd

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

    for pattern in secret_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "MASKED_VALUE",
    "mask_command",
    "mask_secrets",
    "should_mask",
]
