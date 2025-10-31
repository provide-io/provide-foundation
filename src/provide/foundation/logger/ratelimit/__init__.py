#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.logger.ratelimit.limiters import (
    AsyncRateLimiter,
    GlobalRateLimiter,
    SyncRateLimiter,
)
from provide.foundation.logger.ratelimit.processor import (
    RateLimiterProcessor,
    create_rate_limiter_processor,
)
from provide.foundation.logger.ratelimit.queue_limiter import (
    BufferedRateLimiter,
    QueuedRateLimiter,
)

"""Rate limiting subcomponent for Foundation's logging system.
Provides rate limiters and processors for controlling log output rates.
"""

__all__ = [
    "AsyncRateLimiter",
    "BufferedRateLimiter",
    "GlobalRateLimiter",
    "QueuedRateLimiter",
    "RateLimiterProcessor",
    "SyncRateLimiter",
    "create_rate_limiter_processor",
]

# 🧱🏗️🔚
