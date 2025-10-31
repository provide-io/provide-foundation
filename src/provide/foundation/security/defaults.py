#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Security defaults for Foundation configuration."""

# =================================
# Sanitization Defaults
# =================================

# Default sensitive header names (case-insensitive)
DEFAULT_SENSITIVE_HEADERS = [
    "authorization",
    "x-api-key",
    "x-auth-token",
    "cookie",
    "set-cookie",
    "x-csrf-token",
    "x-session-token",
    "proxy-authorization",
]

# Default sensitive URL parameter names (case-insensitive)
DEFAULT_SENSITIVE_PARAMS = [
    "token",
    "key",
    "password",
    "secret",
    "apikey",
    "api_key",
    "access_token",
    "refresh_token",
    "auth",
    "credentials",
]

# Redaction placeholder
REDACTED_VALUE = "[REDACTED]"

# =================================
# Secret Masking Defaults
# =================================

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

__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "DEFAULT_SENSITIVE_HEADERS",
    "DEFAULT_SENSITIVE_PARAMS",
    "MASKED_VALUE",
    "REDACTED_VALUE",
]

# 🧱🏗️🔚
