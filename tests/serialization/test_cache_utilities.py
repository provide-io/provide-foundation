#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from threading import Thread

from provide.foundation.serialization import cache
from provide.foundation.utils.caching import LRUCache


class TestCacheConfiguration:
    """Test cache configuration and lazy initialization."""

    def test_default_cache_enabled(self, clean_env) -> None:
        """Cache should be enabled by default."""
        # Reset module-level variables
        cache.reset_serialization_cache_config()

        enabled = cache.get_cache_enabled()
        assert enabled is True

    def test_default_cache_size(self, clean_env) -> None:
        """Default cache size should be 128."""
        cache.reset_serialization_cache_config()

        size = cache.get_cache_size()
        assert size == 128

    def test_cache_enabled_via_env(self, clean_env, monkeypatch) -> None:
        """Cache can be disabled via environment variable."""
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_ENABLED", "false")
        cache.reset_serialization_cache_config()

        enabled = cache.get_cache_enabled()
        assert enabled is False

    def test_cache_size_via_env(self, clean_env, monkeypatch) -> None:
        """Cache size can be configured via environment variable."""
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "256")
        cache.reset_serialization_cache_config()

        size = cache.get_cache_size()
        assert size == 256

    def test_lazy_initialization_single_call(self, clean_env) -> None:
        """Cache config should only be initialized once."""
        cache.reset_serialization_cache_config()

        # First call initializes
        config1 = cache._get_cache_config()

        # Second call returns cached values
        config2 = cache._get_cache_config()

        assert config1 is config2

    def test_config_persistence_across_calls(self, clean_env, monkeypatch) -> None:
        """Config should persist even if environment changes."""
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "512")
        cache.reset_serialization_cache_config()

        size1 = cache.get_cache_size()

        # Change env (but module level cache should persist)
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "1024")
        size2 = cache.get_cache_size()

        assert size1 == 512
        assert size2 == 512  # Still returns cached value


class TestSerializationCache:
    """Test serialization cache instance management."""

    def test_cache_lazy_initialization(self, clean_env) -> None:
        """Cache instance should be created on first access."""
        cache.reset_serialization_cache_config()

        cache_instance = cache.get_serialization_cache()

        assert isinstance(cache_instance, LRUCache)

    def test_cache_singleton(self, clean_env) -> None:
        """Should return same cache instance on multiple calls."""
        cache.reset_serialization_cache_config()

        cache1 = cache.get_serialization_cache()
        cache2 = cache.get_serialization_cache()

        assert cache1 is cache2

    def test_cache_respects_size_config(self, clean_env, monkeypatch) -> None:
        """Cache should respect configured size limit."""
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "64")
        cache.reset_serialization_cache_config()

        cache_instance = cache.get_serialization_cache()

        assert cache_instance.maxsize == 64

    def test_cache_initialization_creates_lru_cache(self, clean_env) -> None:
        """Cache initialization should create an LRU cache instance."""
        cache.reset_serialization_cache_config()

        cache_instance = cache.get_serialization_cache()

        # Verify it's an LRUCache with expected attributes
        assert hasattr(cache_instance, "maxsize")
        assert hasattr(cache_instance, "get")
        assert hasattr(cache_instance, "set")
        assert hasattr(cache_instance, "clear")


class TestCacheKeyGeneration:
    """Test cache key generation."""

    def test_cache_key_basic(self) -> None:
        """Should generate cache key from content and format."""
        key = cache.get_cache_key('{"test": "data"}', "json")

        assert key.startswith("json:")
        assert len(key) > 6  # format + ':' + hash

    def test_cache_key_deterministic(self) -> None:
        """Same content should generate same key."""
        content = '{"test": "data"}'

        key1 = cache.get_cache_key(content, "json")
        key2 = cache.get_cache_key(content, "json")

        assert key1 == key2

    def test_cache_key_different_content(self) -> None:
        """Different content should generate different keys."""
        key1 = cache.get_cache_key('{"a": 1}', "json")
        key2 = cache.get_cache_key('{"b": 2}', "json")

        assert key1 != key2

    def test_cache_key_different_format(self) -> None:
        """Same content with different format should generate different keys."""
        content = "test: value"

        key1 = cache.get_cache_key(content, "yaml")
        key2 = cache.get_cache_key(content, "toml")

        assert key1 != key2
        assert key1.startswith("yaml:")
        assert key2.startswith("toml:")

    def test_cache_key_empty_content(self) -> None:
        """Should handle empty content."""
        key = cache.get_cache_key("", "json")

        assert key.startswith("json:")

    def test_cache_key_unicode_content(self) -> None:
        """Should handle Unicode content."""
        key = cache.get_cache_key('{"emoji": "🎉"}', "json")

        assert key.startswith("json:")

    def test_cache_key_hash_length(self) -> None:
        """Hash should be truncated to 16 characters."""
        key = cache.get_cache_key("test content", "json")
        hash_part = key.split(":")[1]

        assert len(hash_part) == 16


class TestCacheOperations:
    """Test cache operations."""

    def test_cache_set_and_get(self, clean_env) -> None:
        """Should be able to set and get values."""
        cache.reset_serialization_cache_config()
        cache_instance = cache.get_serialization_cache()

        key = cache.get_cache_key('{"test": 1}', "json")
        cache_instance.set(key, {"test": 1})

        result = cache_instance.get(key)
        assert result == {"test": 1}

    def test_cache_miss_returns_none(self, clean_env) -> None:
        """Cache miss should return None."""
        cache.reset_serialization_cache_config()
        cache_instance = cache.get_serialization_cache()

        result = cache_instance.get("nonexistent:key")
        assert result is None

    def test_cache_clear(self, clean_env) -> None:
        """Should be able to clear cache."""
        cache.reset_serialization_cache_config()
        cache_instance = cache.get_serialization_cache()

        key = cache.get_cache_key('{"test": 1}', "json")
        cache_instance.set(key, {"test": 1})
        cache_instance.clear()

        result = cache_instance.get(key)
        assert result is None

    def test_cache_lru_eviction(self, clean_env, monkeypatch) -> None:
        """Should evict oldest items when cache is full."""
        monkeypatch.setenv("FOUNDATION_SERIALIZATION_CACHE_SIZE", "2")
        cache.reset_serialization_cache_config()

        cache_instance = cache.get_serialization_cache()

        # Fill cache
        cache_instance.set("key1", "value1")
        cache_instance.set("key2", "value2")

        # This should evict key1
        cache_instance.set("key3", "value3")

        assert cache_instance.get("key1") is None
        assert cache_instance.get("key2") == "value2"
        assert cache_instance.get("key3") == "value3"


class TestThreadSafety:
    """Test thread safety of cache operations."""

    def test_concurrent_cache_initialization(self, clean_env) -> None:
        """Multiple threads initializing cache should be safe."""
        cache.reset_serialization_cache_config()
        caches = []

        def init_cache() -> None:
            caches.append(cache.get_serialization_cache())

        threads = [Thread(target=init_cache) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should get the same cache instance
        assert all(c is caches[0] for c in caches)

    def test_concurrent_cache_operations(self, clean_env) -> None:
        """Concurrent cache operations should be safe."""
        cache.reset_serialization_cache_config()
        cache_instance = cache.get_serialization_cache()
        results = []

        def cache_operation(index: int) -> None:
            key = cache.get_cache_key(f"data{index}", "json")
            cache_instance.set(key, {"index": index})
            results.append(cache_instance.get(key))

        threads = [Thread(target=cache_operation, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All operations should complete successfully
        assert len(results) == 20
        assert all(r is not None for r in results)


class TestConvenienceConstants:
    """Test convenience constant functions."""

    def test_cache_enabled_constant(self, clean_env) -> None:
        """CACHE_ENABLED should be callable."""
        cache.reset_serialization_cache_config()

        assert callable(cache.CACHE_ENABLED)
        assert cache.CACHE_ENABLED() is True

    def test_cache_size_constant(self, clean_env) -> None:
        """CACHE_SIZE should be callable."""
        cache.reset_serialization_cache_config()

        assert callable(cache.CACHE_SIZE)
        assert cache.CACHE_SIZE() == 128

    def test_serialization_cache_constant(self, clean_env) -> None:
        """serialization_cache should be callable."""
        cache.reset_serialization_cache_config()

        assert callable(cache.serialization_cache)
        assert isinstance(cache.serialization_cache(), LRUCache)


class TestModuleExports:
    """Test module exports."""

    def test_all_exports(self) -> None:
        """Module should export expected symbols."""
        expected = ["CACHE_ENABLED", "CACHE_SIZE", "get_cache_key", "serialization_cache"]

        assert set(cache.__all__) == set(expected)

    def test_exported_symbols_accessible(self) -> None:
        """All exported symbols should be accessible."""
        for symbol in cache.__all__:
            assert hasattr(cache, symbol)


# 🧱🏗️🔚
