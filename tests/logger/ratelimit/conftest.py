#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test fixtures for rate limiter tests."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from provide.foundation.logger.ratelimit.queue_limiter import QueuedRateLimiter


@pytest.fixture
def ensure_limiter_cleanup() -> Generator[Callable[[QueuedRateLimiter], QueuedRateLimiter], None, None]:
    """Fixture that ensures QueuedRateLimiter cleanup after test.

    Usage:
        def test_something(ensure_limiter_cleanup):
            limiter = ensure_limiter_cleanup(QueuedRateLimiter(...))
            # Test code here
            # Limiter will be automatically stopped after test
    """
    limiters: list[QueuedRateLimiter] = []

    def register_limiter(limiter: QueuedRateLimiter) -> QueuedRateLimiter:
        limiters.append(limiter)
        return limiter

    yield register_limiter

    # Cleanup all registered limiters
    for limiter in limiters:
        if limiter.running:
            limiter.stop()


# 🧱🏗️🔚
