"""
Tests for fallback functionality.
"""

import asyncio
from unittest.mock import MagicMock

import pytest

from provide.foundation.resilience.fallback import FallbackChain, fallback


class TestFallbackChain:
    """Test FallbackChain class."""
    
    def test_primary_success_no_fallbacks_used(self):
        """Test successful primary function doesn't use fallbacks."""
        chain = FallbackChain()
        
        fallback_func = MagicMock(return_value="fallback")
        chain.add_fallback(fallback_func)
        
        def primary_func():
            return "primary"
        
        result = chain.execute(primary_func)
        
        assert result == "primary"
        fallback_func.assert_not_called()
    
    def test_primary_failure_uses_fallback(self):
        """Test primary failure triggers fallback."""
        chain = FallbackChain()
        
        def fallback_func():
            return "fallback result"
        
        chain.add_fallback(fallback_func)
        
        def primary_func():
            raise ValueError("primary failed")
        
        result = chain.execute(primary_func)
        
        assert result == "fallback result"
    
    def test_multiple_fallbacks_in_order(self):
        """Test multiple fallbacks are tried in order."""
        chain = FallbackChain()
        
        def fallback1():
            raise ValueError("fallback1 failed")
        
        def fallback2():
            return "fallback2 success"
        
        def fallback3():
            return "fallback3 success"
        
        chain.add_fallback(fallback1)
        chain.add_fallback(fallback2)
        chain.add_fallback(fallback3)
        
        def primary_func():
            raise ValueError("primary failed")
        
        result = chain.execute(primary_func)
        
        assert result == "fallback2 success"
    
    def test_all_fallbacks_fail(self):
        """Test behavior when all fallbacks fail."""
        chain = FallbackChain()
        
        def fallback1():
            raise ValueError("fallback1 failed")
        
        def fallback2():
            raise RuntimeError("fallback2 failed")
        
        chain.add_fallback(fallback1)
        chain.add_fallback(fallback2)
        
        def primary_func():
            raise ValueError("primary failed")
        
        # Should raise the last fallback exception
        with pytest.raises(RuntimeError, match="fallback2 failed"):
            chain.execute(primary_func)
    
    def test_unexpected_exception_type_skips_fallbacks(self):
        """Test unexpected exception types skip fallback chain."""
        chain = FallbackChain(expected_exceptions=(ValueError,))
        
        fallback_func = MagicMock()
        chain.add_fallback(fallback_func)
        
        def primary_func():
            raise RuntimeError("unexpected error")
        
        with pytest.raises(RuntimeError, match="unexpected error"):
            chain.execute(primary_func)
        
        fallback_func.assert_not_called()
    
    def test_fallback_with_arguments(self):
        """Test fallback chain passes arguments correctly."""
        chain = FallbackChain()
        
        def fallback_func(x, y, z=None):
            return f"fallback: {x}-{y}-{z}"
        
        chain.add_fallback(fallback_func)
        
        def primary_func(x, y, z=None):
            raise ValueError("primary failed")
        
        result = chain.execute(primary_func, "a", "b", z="c")
        
        assert result == "fallback: a-b-c"
    
    @pytest.mark.asyncio
    async def test_async_fallback_chain(self):
        """Test fallback chain with async functions."""
        chain = FallbackChain()
        
        async def async_fallback():
            return "async fallback"
        
        chain.add_fallback(async_fallback)
        
        async def async_primary():
            raise ValueError("async primary failed")
        
        result = await chain.execute_async(async_primary)
        
        assert result == "async fallback"
    
    @pytest.mark.asyncio
    async def test_mixed_sync_async_fallbacks(self):
        """Test mixing sync and async fallbacks."""
        chain = FallbackChain()
        
        def sync_fallback():
            return "sync fallback"
        
        async def async_fallback():
            return "async fallback"
        
        chain.add_fallback(sync_fallback)
        chain.add_fallback(async_fallback)
        
        async def async_primary():
            raise ValueError("async primary failed")
        
        result = await chain.execute_async(async_primary)
        
        assert result == "sync fallback"
    
    def test_no_fallbacks_configured(self):
        """Test chain with no fallbacks configured."""
        chain = FallbackChain()
        
        def primary_func():
            raise ValueError("primary failed")
        
        with pytest.raises(ValueError, match="primary failed"):
            chain.execute(primary_func)


class TestFallbackDecorator:
    """Test @fallback decorator."""
    
    def test_fallback_decorator_success(self):
        """Test fallback decorator with successful primary function."""
        
        def backup_func():
            return "backup"
        
        @fallback(backup_func)
        def primary_func():
            return "primary"
        
        result = primary_func()
        assert result == "primary"
    
    def test_fallback_decorator_failure(self):
        """Test fallback decorator with failing primary function."""
        
        def backup_func():
            return "backup"
        
        @fallback(backup_func)
        def primary_func():
            raise ValueError("primary failed")
        
        result = primary_func()
        assert result == "backup"
    
    def test_multiple_fallbacks_decorator(self):
        """Test fallback decorator with multiple fallbacks."""
        
        def backup1():
            raise ValueError("backup1 failed")
        
        def backup2():
            return "backup2 success"
        
        @fallback(backup1, backup2)
        def primary_func():
            raise ValueError("primary failed")
        
        result = primary_func()
        assert result == "backup2 success"
    
    @pytest.mark.asyncio
    async def test_async_fallback_decorator(self):
        """Test fallback decorator with async functions."""
        
        async def async_backup():
            return "async backup"
        
        @fallback(async_backup)
        async def async_primary():
            raise ValueError("async primary failed")
        
        result = await async_primary()
        assert result == "async backup"
    
    def test_fallback_decorator_with_arguments(self):
        """Test fallback decorator preserves function arguments."""
        
        def backup_func(x, y=None):
            return f"backup: {x}-{y}"
        
        @fallback(backup_func)
        def primary_func(x, y=None):
            raise ValueError("primary failed")
        
        result = primary_func("test", y="value")
        assert result == "backup: test-value"
    
    def test_fallback_decorator_preserves_metadata(self):
        """Test fallback decorator preserves function metadata."""
        
        def backup_func():
            return "backup"
        
        @fallback(backup_func)
        def primary_func():
            """Primary function docstring."""
            return "primary"
        
        assert primary_func.__name__ == "primary_func"
        assert primary_func.__doc__ == "Primary function docstring."