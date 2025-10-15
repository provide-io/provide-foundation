# provide/foundation/security/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.security.masking import (
    DEFAULT_SECRET_PATTERNS,
    MASKED_VALUE,
    mask_command,
    mask_secrets,
    should_mask,
)
from provide.foundation.security.sanitization import (
    DEFAULT_SENSITIVE_HEADERS,
    DEFAULT_SENSITIVE_PARAMS,
    REDACTED_VALUE,
    sanitize_dict,
    sanitize_headers,
    sanitize_uri,
    should_sanitize_body,
)

"""Security utilities for Foundation."""

__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "DEFAULT_SENSITIVE_HEADERS",
    "DEFAULT_SENSITIVE_PARAMS",
    "MASKED_VALUE",
    "REDACTED_VALUE",
    "mask_command",
    "mask_secrets",
    "sanitize_dict",
    "sanitize_headers",
    "sanitize_uri",
    "should_mask",
    "should_sanitize_body",
]


# <3 🧱🤝🛡️🪄
