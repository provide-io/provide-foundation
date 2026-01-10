#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for fallback functionality."""

from __future__ import annotations

from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock
import pytest

from provide.foundation.resilience.fallback import FallbackChain, fallback


class TestFallbackChain(FoundationTestCase):
    """Test FallbackChain class."""

    def test_primary_success_no_fallbacks_used(self) -> None:
        """Test successful primary function doesn't use fallbacks."""
        chain = FallbackChain()

        fallback_func = MagicMock(return_value="fallback")
        chain.add_fallback(fallback_func)

        def primary_func() -> str:
            return "primary"

        result = chain.execute(primary_func)

        assert result == "primary"
        fallback_func.assert_not_called()

    def test_primary_failure_uses_fallback(self) -> None:
        """Test primary failure triggers fallback."""
        chain = FallbackChain()

        def fallback_func() -> str:
            return "fallback result"

        chain.add_fallback(fallback_func)

        def primary_func() -> Never:
            raise ValueError("primary failed")

        result = chain.execute(primary_func)

        assert result == "fallback result"

    def test_multiple_fallbacks_in_order(self) -> None:
        """Test multiple fallbacks are tried in order."""
        chain = FallbackChain()

        def fallback1() -> Never:
            raise ValueError("fallback1 failed")

        def fallback2() -> str:
            return "fallback2 success"

        def fallback3() -> str:
            return "fallback3 success"

        chain.add_fallback(fallback1)
        chain.add_fallback(fallback2)
        chain.add_fallback(fallback3)

        def primary_func() -> Never:
            raise ValueError("primary failed")

        result = chain.execute(primary_func)

        assert result == "fallback2 success"

    def test_all_fallbacks_fail(self) -> None:
        """Test behavior when all fallbacks fail."""
        chain = FallbackChain()

        def fallback1() -> Never:
            raise ValueError("fallback1 failed")

        def fallback2() -> Never:
            raise RuntimeError("fallback2 failed")

        chain.add_fallback(fallback1)
        chain.add_fallback(fallback2)

        def primary_func() -> Never:
            raise ValueError("primary failed")

        # Should raise the last fallback exception
        with pytest.raises(RuntimeError, match="fallback2 failed"):
            chain.execute(primary_func)

    def test_unexpected_exception_type_skips_fallbacks(self) -> None:
        """Test unexpected exception types skip fallback chain."""
        chain = FallbackChain(expected_exceptions=(ValueError,))

        fallback_func = MagicMock()
        chain.add_fallback(fallback_func)

        def primary_func() -> Never:
            raise RuntimeError("unexpected error")

        with pytest.raises(RuntimeError, match="unexpected error"):
            chain.execute(primary_func)

        fallback_func.assert_not_called()

    def test_fallback_with_arguments(self) -> None:
        """Test fallback chain passes arguments correctly."""
        chain = FallbackChain()

        def fallback_func(x: str, y: str, z: str | None = None) -> str:
            return f"fallback: {x}-{y}-{z}"

        chain.add_fallback(fallback_func)

        def primary_func(x: str, y: str, z: str | None = None) -> Never:
            raise ValueError("primary failed")

        result = chain.execute(primary_func, "a", "b", z="c")

        assert result == "fallback: a-b-c"

    @pytest.mark.asyncio
    async def test_async_fallback_chain(self) -> None:
        """Test fallback chain with async functions."""
        chain = FallbackChain()

        async def async_fallback() -> str:
            return "async fallback"

        chain.add_fallback(async_fallback)

        async def async_primary() -> Never:
            raise ValueError("async primary failed")

        result = await chain.execute_async(async_primary)

        assert result == "async fallback"

    @pytest.mark.asyncio
    async def test_mixed_sync_async_fallbacks(self) -> None:
        """Test mixing sync and async fallbacks."""
        chain = FallbackChain()

        def sync_fallback() -> str:
            return "sync fallback"

        async def async_fallback() -> str:
            return "async fallback"

        chain.add_fallback(sync_fallback)
        chain.add_fallback(async_fallback)

        async def async_primary() -> Never:
            raise ValueError("async primary failed")

        result = await chain.execute_async(async_primary)

        assert result == "sync fallback"

    def test_no_fallbacks_configured(self) -> None:
        """Test chain with no fallbacks configured."""
        chain = FallbackChain()

        def primary_func() -> Never:
            raise ValueError("primary failed")

        with pytest.raises(ValueError, match="primary failed"):
            chain.execute(primary_func)


class TestFallbackDecorator(FoundationTestCase):
    """Test @fallback decorator."""

    def test_fallback_decorator_success(self) -> None:
        """Test fallback decorator with successful primary function."""

        def backup_func() -> str:
            return "backup"

        @fallback(backup_func)
        def primary_func() -> str:
            return "primary"

        result = primary_func()
        assert result == "primary"

    def test_fallback_decorator_failure(self) -> None:
        """Test fallback decorator with failing primary function."""

        def backup_func() -> str:
            return "backup"

        @fallback(backup_func)
        def primary_func() -> Never:
            raise ValueError("primary failed")

        result = primary_func()
        assert result == "backup"

    def test_multiple_fallbacks_decorator(self) -> None:
        """Test fallback decorator with multiple fallbacks."""

        def backup1() -> Never:
            raise ValueError("backup1 failed")

        def backup2() -> str:
            return "backup2 success"

        @fallback(backup1, backup2)
        def primary_func() -> Never:
            raise ValueError("primary failed")

        result = primary_func()
        assert result == "backup2 success"

    @pytest.mark.asyncio
    async def test_async_fallback_decorator(self) -> None:
        """Test fallback decorator with async functions."""

        async def async_backup() -> str:
            return "async backup"

        @fallback(async_backup)
        async def async_primary() -> Never:
            raise ValueError("async primary failed")

        result = await async_primary()
        assert result == "async backup"

    def test_fallback_decorator_with_arguments(self) -> None:
        """Test fallback decorator preserves function arguments."""

        def backup_func(x: str, y: str | None = None) -> str:
            return f"backup: {x}-{y}"

        @fallback(backup_func)
        def primary_func(x: str, y: str | None = None) -> Never:
            raise ValueError("primary failed")

        result = primary_func("test", y="value")
        assert result == "backup: test-value"

    def test_fallback_decorator_preserves_metadata(self) -> None:
        """Test fallback decorator preserves function metadata."""

        def backup_func() -> str:
            return "backup"

        @fallback(backup_func)
        def primary_func() -> str:
            """Primary function docstring."""
            return "primary"

        assert primary_func.__name__ == "primary_func"
        assert primary_func.__doc__ == "Primary function docstring."


# 🧱🏗️🔚
