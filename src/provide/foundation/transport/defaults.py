#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Transport defaults for Foundation configuration."""

# =================================
# Transport Defaults
# =================================
DEFAULT_TRANSPORT_TIMEOUT = 30.0
DEFAULT_TRANSPORT_MAX_RETRIES = 3
DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR = 0.5
DEFAULT_TRANSPORT_VERIFY_SSL = True

# =================================
# HTTP Transport Defaults
# =================================
DEFAULT_HTTP_POOL_CONNECTIONS = 10
DEFAULT_HTTP_POOL_MAXSIZE = 100
DEFAULT_HTTP_FOLLOW_REDIRECTS = True
DEFAULT_HTTP_USE_HTTP2 = False
DEFAULT_HTTP_MAX_REDIRECTS = 5

# =================================
# Transport Middleware Defaults
# =================================
DEFAULT_TRANSPORT_LOG_REQUESTS = True
DEFAULT_TRANSPORT_LOG_RESPONSES = True
DEFAULT_TRANSPORT_LOG_BODIES = False

# =================================
# Transport Cache Defaults
# =================================
DEFAULT_TRANSPORT_FAILURE_THRESHOLD = 3

__all__ = [
    "DEFAULT_HTTP_FOLLOW_REDIRECTS",
    "DEFAULT_HTTP_MAX_REDIRECTS",
    "DEFAULT_HTTP_POOL_CONNECTIONS",
    "DEFAULT_HTTP_POOL_MAXSIZE",
    "DEFAULT_HTTP_USE_HTTP2",
    "DEFAULT_TRANSPORT_FAILURE_THRESHOLD",
    "DEFAULT_TRANSPORT_LOG_BODIES",
    "DEFAULT_TRANSPORT_LOG_REQUESTS",
    "DEFAULT_TRANSPORT_LOG_RESPONSES",
    "DEFAULT_TRANSPORT_MAX_RETRIES",
    "DEFAULT_TRANSPORT_RETRY_BACKOFF_FACTOR",
    "DEFAULT_TRANSPORT_TIMEOUT",
    "DEFAULT_TRANSPORT_VERIFY_SSL",
]

# 🧱🏗️🔚
