#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from attrs import define, field

from provide.foundation.logger import get_logger
from provide.foundation.transport.defaults import DEFAULT_TRANSPORT_FAILURE_THRESHOLD
from provide.foundation.transport.errors import TransportCacheEvictedError

"""Transport cache with health tracking and automatic eviction."""

log = get_logger(__name__)


@define(slots=True)
class TransportHealth:
    """Health tracking for a transport instance."""

    consecutive_failures: int = field(default=0)
    total_requests: int = field(default=0)
    total_failures: int = field(default=0)

    def record_success(self) -> None:
        """Record a successful request."""
        self.total_requests += 1
        self.consecutive_failures = 0

    def record_failure(self) -> None:
        """Record a failed request."""
        self.total_requests += 1
        self.total_failures += 1
        self.consecutive_failures += 1

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        if self.total_requests == 0:
            return 0.0
        return self.total_failures / self.total_requests


@define(slots=True)
class TransportCache:
    """Transport cache with automatic health-based eviction.

    Tracks transport health and automatically evicts transports that
    exceed the failure threshold. This prevents cascading failures from
    unhealthy transports.
    """

    failure_threshold: int = field(default=DEFAULT_TRANSPORT_FAILURE_THRESHOLD)
    _transports: dict[str, Any] = field(factory=dict, init=False)
    _health: dict[str, TransportHealth] = field(factory=dict, init=False)
    _evicted: set[str] = field(factory=set, init=False)

    async def get_or_create(
        self,
        scheme: str,
        factory: Callable[[str], Any],
    ) -> Any:
        """Get or create transport for scheme.

        Args:
            scheme: Transport scheme (e.g., "http", "https")
            factory: Factory function to create new transport

        Returns:
            Transport instance

        Raises:
            TransportCacheEvictedError: If transport was evicted due to failures
        """
        # Check if transport was evicted
        if scheme in self._evicted:
            raise TransportCacheEvictedError(
                f"Transport '{scheme}' was evicted due to {self.failure_threshold} consecutive failures. "
                f"Clear cache or create new client to retry.",
                scheme=scheme,
                consecutive_failures=self.failure_threshold,
            )

        # Get or create transport
        if scheme not in self._transports:
            transport = factory(scheme)
            await transport.connect()
            self._transports[scheme] = transport
            self._health[scheme] = TransportHealth()

        return self._transports[scheme]

    def mark_success(self, scheme: str) -> None:
        """Mark a successful request for scheme.

        Args:
            scheme: Transport scheme
        """
        if scheme in self._health:
            self._health[scheme].record_success()

    def mark_failure(self, scheme: str, error: Exception) -> None:
        """Mark a failed request for scheme.

        Automatically evicts transport if failure threshold is exceeded.

        Args:
            scheme: Transport scheme
            error: Error that occurred
        """
        if scheme not in self._health:
            # Transport not in cache, nothing to track
            return

        health = self._health[scheme]
        health.record_failure()

        log.warning(
            "⚠️ Transport request failed",
            scheme=scheme,
            consecutive_failures=health.consecutive_failures,
            failure_rate=f"{health.failure_rate:.2%}",
            error=str(error),
        )

        # Check if we should evict (threshold=0 disables eviction)
        if self.failure_threshold > 0 and health.consecutive_failures >= self.failure_threshold:
            self.evict(scheme)
            log.error(
                "🚫 Transport evicted due to consecutive failures",
                scheme=scheme,
                consecutive_failures=health.consecutive_failures,
                total_failures=health.total_failures,
                total_requests=health.total_requests,
            )

    def evict(self, scheme: str) -> None:
        """Evict transport from cache.

        Args:
            scheme: Transport scheme to evict
        """
        if scheme in self._transports:
            log.info("🗑️ Evicting transport", scheme=scheme)
            # Don't await disconnect - caller handles cleanup
            self._transports.pop(scheme, None)
            self._health.pop(scheme, None)
            self._evicted.add(scheme)

    def get_health(self, scheme: str) -> TransportHealth | None:
        """Get health status for scheme.

        Args:
            scheme: Transport scheme

        Returns:
            TransportHealth or None if not tracked
        """
        return self._health.get(scheme)

    def clear(self) -> dict[str, Any]:
        """Clear all cached transports.

        Returns:
            Dictionary of evicted transports for cleanup
        """
        log.debug("🧹 Clearing transport cache", count=len(self._transports))
        transports = dict(self._transports)
        self._transports.clear()
        self._health.clear()
        self._evicted.clear()
        return transports

    def is_evicted(self, scheme: str) -> bool:
        """Check if transport was evicted.

        Args:
            scheme: Transport scheme

        Returns:
            True if transport was evicted
        """
        return scheme in self._evicted


__all__ = [
    "TransportCache",
    "TransportHealth",
]

# 🧱🏗️🔚
