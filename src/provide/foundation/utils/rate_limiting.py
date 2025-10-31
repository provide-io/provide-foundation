#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import time
from typing import final

"""Rate limiting utilities for Foundation.

This module provides rate limiting implementations suitable for
asynchronous applications, helping to manage request load and prevent abuse.
"""


@final
class TokenBucketRateLimiter:
    """A Token Bucket rate limiter for asyncio applications.

    This limiter allows for bursts up to a specified capacity and refills tokens
    at a constant rate. It is designed to be thread-safe using an asyncio.Lock.
    """

    def __init__(
        self,
        capacity: float,
        refill_rate: float,
        time_source: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the TokenBucketRateLimiter.

        Args:
            capacity: The maximum number of tokens the bucket can hold
                      (burst capacity).
            refill_rate: The rate at which tokens are refilled per second.
            time_source: Optional callable that returns current time (for testing).
                        Defaults to time.monotonic.

        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive.")

        self._capacity: float = float(capacity)
        self._refill_rate: float = float(refill_rate)
        self._tokens: float = float(capacity)  # Start with a full bucket
        self._time_source = time_source if time_source is not None else time.monotonic
        self._last_refill_timestamp: float = self._time_source()
        self._lock = asyncio.Lock()

        # Cache logger instance to avoid repeated imports
        self._logger = None
        try:
            from provide.foundation.logger import get_logger

            self._logger = get_logger(__name__)
            self._logger.debug(
                f"🔩🗑️ TokenBucketRateLimiter initialized: capacity={capacity}, refill_rate={refill_rate}",
            )
        except ImportError:
            # Fallback if logger not available
            pass

    async def _refill_tokens(self) -> None:
        """Refills tokens based on the elapsed time since the last refill.
        This method is not locked internally; caller must hold the lock.
        """
        now = self._time_source()
        elapsed_time = now - self._last_refill_timestamp
        if elapsed_time > 0:  # only refill if time has passed
            tokens_to_add = elapsed_time * self._refill_rate
            # logger.debug(
            #     f"🔩🗑️ Refilling: elapsed={elapsed_time:.4f}s, "
            #     f"tokens_to_add={tokens_to_add:.4f}, "
            #     f"current_tokens={self._tokens:.4f}"
            # )
            self._tokens = min(self._capacity, self._tokens + tokens_to_add)
            self._last_refill_timestamp = now
            # logger.debug(
            #     f"🔩🗑️ Refilled: new_tokens={self._tokens:.4f}, "
            #     f"last_refill_timestamp={self._last_refill_timestamp:.4f}"
            # )

    async def is_allowed(self) -> bool:
        """Check if a request is allowed based on available tokens.

        This method is asynchronous and thread-safe. It refills tokens
        based on elapsed time and then attempts to consume a token.

        Returns:
            True if the request is allowed, False otherwise.

        """
        async with self._lock:
            await self._refill_tokens()  # Refill before checking

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                if self._logger:
                    self._logger.debug(
                        f"🔩✅ Request allowed. Tokens remaining: {self._tokens:.2f}/{self._capacity:.2f}",
                    )
                return True
            if self._logger:
                self._logger.warning(
                    "🔩🗑️❌ Request denied. No tokens available. Tokens: "
                    f"{self._tokens:.2f}/{self._capacity:.2f}",
                )
            return False

    async def get_current_tokens(self) -> float:
        """Returns the current number of tokens, for testing/monitoring."""
        async with self._lock:
            # It might be useful to refill before getting, to get the most
            # up-to-date count
            # await self._refill_tokens()
            return self._tokens


# 🧱🏗️🔚
