#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for transport cache with health tracking."""

from __future__ import annotations

from provide.testkit.mocking import AsyncMock, MagicMock
import pytest

from provide.foundation.transport.cache import TransportCache, TransportHealth
from provide.foundation.transport.errors import TransportCacheEvictedError, TransportError


class TestTransportHealth:
    """Test TransportHealth tracking."""

    def test_initial_state(self) -> None:
        """Test health starts with zero counts."""
        health = TransportHealth()
        assert health.consecutive_failures == 0
        assert health.total_requests == 0
        assert health.total_failures == 0
        assert health.failure_rate == 0.0

    def test_record_success(self) -> None:
        """Test recording successful requests."""
        health = TransportHealth()
        health.record_success()
        assert health.total_requests == 1
        assert health.total_failures == 0
        assert health.consecutive_failures == 0
        assert health.failure_rate == 0.0

    def test_record_failure(self) -> None:
        """Test recording failed requests."""
        health = TransportHealth()
        health.record_failure()
        assert health.total_requests == 1
        assert health.total_failures == 1
        assert health.consecutive_failures == 1
        assert health.failure_rate == 1.0

    def test_consecutive_failures_reset_on_success(self) -> None:
        """Test consecutive failures reset after success."""
        health = TransportHealth()
        health.record_failure()
        health.record_failure()
        assert health.consecutive_failures == 2

        health.record_success()
        assert health.consecutive_failures == 0
        assert health.total_failures == 2  # Total not reset
        assert health.total_requests == 3

    def test_failure_rate_calculation(self) -> None:
        """Test failure rate is calculated correctly."""
        health = TransportHealth()
        health.record_success()
        health.record_failure()
        health.record_success()
        health.record_failure()
        health.record_failure()

        assert health.total_requests == 5
        assert health.total_failures == 3
        assert health.failure_rate == 0.6  # 3/5


class TestTransportCacheBasics:
    """Test basic transport cache operations."""

    @pytest.mark.asyncio
    async def test_get_or_create_new_transport(self) -> None:
        """Test creating new transport via cache."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        result = await cache.get_or_create("http", factory)
        assert result is mock_transport
        mock_transport.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_or_create_cached_transport(self) -> None:
        """Test retrieving cached transport."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        # First call creates
        result1 = await cache.get_or_create("http", factory)
        # Second call retrieves from cache
        result2 = await cache.get_or_create("http", factory)

        assert result1 is result2
        assert mock_transport.connect.call_count == 1  # Only called once

    @pytest.mark.asyncio
    async def test_get_or_create_different_schemes(self) -> None:
        """Test different schemes create different transports."""
        cache = TransportCache()
        http_transport = MagicMock()
        http_transport.connect = AsyncMock()
        https_transport = MagicMock()
        https_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            if scheme == "http":
                return http_transport
            else:
                return https_transport

        http_result = await cache.get_or_create("http", factory)
        https_result = await cache.get_or_create("https", factory)

        assert http_result is http_transport
        assert https_result is https_transport
        assert http_result is not https_result


class TestTransportCacheHealthTracking:
    """Test cache health tracking."""

    @pytest.mark.asyncio
    async def test_mark_success_tracks_health(self) -> None:
        """Test marking success updates health."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)
        cache.mark_success("http")

        health = cache.get_health("http")
        assert health is not None
        assert health.total_requests == 1
        assert health.consecutive_failures == 0

    @pytest.mark.asyncio
    async def test_mark_failure_tracks_health(self) -> None:
        """Test marking failure updates health."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)
        error = TransportError("Test error")
        cache.mark_failure("http", error)

        health = cache.get_health("http")
        assert health is not None
        assert health.total_requests == 1
        assert health.total_failures == 1
        assert health.consecutive_failures == 1

    @pytest.mark.asyncio
    async def test_mark_failure_on_uncached_transport(self) -> None:
        """Test marking failure on transport not in cache is safe."""
        cache = TransportCache()
        error = TransportError("Test error")
        cache.mark_failure("nonexistent", error)  # Should not raise

        health = cache.get_health("nonexistent")
        assert health is None


class TestTransportCacheEviction:
    """Test automatic cache eviction."""

    @pytest.mark.asyncio
    async def test_eviction_after_threshold_failures(self) -> None:
        """Test transport is evicted after consecutive failures."""
        cache = TransportCache(failure_threshold=3)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)

        # Record failures up to threshold
        error = TransportError("Test error")
        cache.mark_failure("http", error)
        cache.mark_failure("http", error)
        assert not cache.is_evicted("http")

        cache.mark_failure("http", error)  # Third failure triggers eviction
        assert cache.is_evicted("http")

    @pytest.mark.asyncio
    async def test_evicted_transport_raises_error(self) -> None:
        """Test accessing evicted transport raises error."""
        cache = TransportCache(failure_threshold=2)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)

        # Trigger eviction
        error = TransportError("Test error")
        cache.mark_failure("http", error)
        cache.mark_failure("http", error)

        # Subsequent access should raise
        with pytest.raises(TransportCacheEvictedError) as exc_info:
            await cache.get_or_create("http", factory)

        assert "http" in str(exc_info.value)
        assert exc_info.value.scheme == "http"
        assert exc_info.value.consecutive_failures == 2

    @pytest.mark.asyncio
    async def test_success_prevents_eviction(self) -> None:
        """Test success resets consecutive failures."""
        cache = TransportCache(failure_threshold=3)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)

        # Two failures
        error = TransportError("Test error")
        cache.mark_failure("http", error)
        cache.mark_failure("http", error)

        # Success resets consecutive count
        cache.mark_success("http")

        # Two more failures should not trigger eviction (need 3 consecutive)
        cache.mark_failure("http", error)
        cache.mark_failure("http", error)
        assert not cache.is_evicted("http")

        # Third consecutive failure triggers eviction
        cache.mark_failure("http", error)
        assert cache.is_evicted("http")

    @pytest.mark.asyncio
    async def test_manual_eviction(self) -> None:
        """Test manual transport eviction."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)
        assert not cache.is_evicted("http")

        cache.evict("http")
        assert cache.is_evicted("http")

        # Should raise on subsequent access
        with pytest.raises(TransportCacheEvictedError):
            await cache.get_or_create("http", factory)


class TestTransportCacheClear:
    """Test cache clearing."""

    @pytest.mark.asyncio
    async def test_clear_removes_all_transports(self) -> None:
        """Test clear() removes all cached transports."""
        cache = TransportCache()
        http_transport = MagicMock()
        http_transport.connect = AsyncMock()
        https_transport = MagicMock()
        https_transport.connect = AsyncMock()

        def http_factory(scheme: str) -> MagicMock:
            return http_transport

        def https_factory(scheme: str) -> MagicMock:
            return https_transport

        await cache.get_or_create("http", http_factory)
        await cache.get_or_create("https", https_factory)

        transports = cache.clear()

        assert len(transports) == 2
        assert "http" in transports
        assert "https" in transports
        assert transports["http"] is http_transport
        assert transports["https"] is https_transport

    @pytest.mark.asyncio
    async def test_clear_resets_eviction_state(self) -> None:
        """Test clear() resets evicted transports."""
        cache = TransportCache(failure_threshold=1)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)
        error = TransportError("Test error")
        cache.mark_failure("http", error)
        assert cache.is_evicted("http")

        cache.clear()
        assert not cache.is_evicted("http")

        # Should be able to create again
        result = await cache.get_or_create("http", factory)
        assert result is mock_transport

    @pytest.mark.asyncio
    async def test_clear_resets_health(self) -> None:
        """Test clear() resets health tracking."""
        cache = TransportCache()
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)
        cache.mark_success("http")
        assert cache.get_health("http") is not None

        cache.clear()
        assert cache.get_health("http") is None


class TestTransportCacheCustomThreshold:
    """Test custom failure thresholds."""

    @pytest.mark.asyncio
    async def test_custom_threshold_respected(self) -> None:
        """Test custom failure threshold is respected."""
        cache = TransportCache(failure_threshold=5)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)

        error = TransportError("Test error")
        for _ in range(4):
            cache.mark_failure("http", error)
            assert not cache.is_evicted("http")

        cache.mark_failure("http", error)  # 5th failure
        assert cache.is_evicted("http")

    @pytest.mark.asyncio
    async def test_zero_threshold_never_evicts(self) -> None:
        """Test threshold of 0 prevents eviction."""
        cache = TransportCache(failure_threshold=0)
        mock_transport = MagicMock()
        mock_transport.connect = AsyncMock()

        def factory(scheme: str) -> MagicMock:
            return mock_transport

        await cache.get_or_create("http", factory)

        error = TransportError("Test error")
        for _ in range(100):
            cache.mark_failure("http", error)

        # Should never evict with threshold=0
        assert not cache.is_evicted("http")


# 🧱🏗️🔚
