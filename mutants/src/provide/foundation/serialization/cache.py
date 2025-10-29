# provide/foundation/serialization/cache.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.serialization.config import SerializationCacheConfig
    from provide.foundation.utils.caching import LRUCache

"""Caching utilities for serialization operations."""

# Cache configuration - lazy evaluation to avoid circular imports
_cached_config: SerializationCacheConfig | None = None
_serialization_cache: LRUCache | None = None
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__get_cache_config__mutmut_orig() -> SerializationCacheConfig:
    """Get cache configuration with lazy initialization."""
    global _cached_config
    if _cached_config is None:
        from provide.foundation.serialization.config import SerializationCacheConfig

        _cached_config = SerializationCacheConfig.from_env()
    return _cached_config


def x__get_cache_config__mutmut_1() -> SerializationCacheConfig:
    """Get cache configuration with lazy initialization."""
    global _cached_config
    if _cached_config is not None:
        from provide.foundation.serialization.config import SerializationCacheConfig

        _cached_config = SerializationCacheConfig.from_env()
    return _cached_config


def x__get_cache_config__mutmut_2() -> SerializationCacheConfig:
    """Get cache configuration with lazy initialization."""
    global _cached_config
    if _cached_config is None:
        from provide.foundation.serialization.config import SerializationCacheConfig

        _cached_config = None
    return _cached_config


x__get_cache_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_cache_config__mutmut_1": x__get_cache_config__mutmut_1,
    "x__get_cache_config__mutmut_2": x__get_cache_config__mutmut_2,
}


def _get_cache_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_cache_config__mutmut_orig, x__get_cache_config__mutmut_mutants, args, kwargs
    )
    return result


_get_cache_config.__signature__ = _mutmut_signature(x__get_cache_config__mutmut_orig)
x__get_cache_config__mutmut_orig.__name__ = "x__get_cache_config"


def x_get_cache_enabled__mutmut_orig() -> bool:
    """Whether caching is enabled."""
    config = _get_cache_config()
    return config.cache_enabled


def x_get_cache_enabled__mutmut_1() -> bool:
    """Whether caching is enabled."""
    config = None
    return config.cache_enabled


x_get_cache_enabled__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_cache_enabled__mutmut_1": x_get_cache_enabled__mutmut_1
}


def get_cache_enabled(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_cache_enabled__mutmut_orig, x_get_cache_enabled__mutmut_mutants, args, kwargs
    )
    return result


get_cache_enabled.__signature__ = _mutmut_signature(x_get_cache_enabled__mutmut_orig)
x_get_cache_enabled__mutmut_orig.__name__ = "x_get_cache_enabled"


def x_get_cache_size__mutmut_orig() -> int:
    """Cache size limit."""
    config = _get_cache_config()
    return config.cache_size


def x_get_cache_size__mutmut_1() -> int:
    """Cache size limit."""
    config = None
    return config.cache_size


x_get_cache_size__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_cache_size__mutmut_1": x_get_cache_size__mutmut_1
}


def get_cache_size(*args, **kwargs):
    result = _mutmut_trampoline(x_get_cache_size__mutmut_orig, x_get_cache_size__mutmut_mutants, args, kwargs)
    return result


get_cache_size.__signature__ = _mutmut_signature(x_get_cache_size__mutmut_orig)
x_get_cache_size__mutmut_orig.__name__ = "x_get_cache_size"


def x_get_serialization_cache__mutmut_orig() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_1() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is not None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_2() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = None
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_3() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = None
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_4() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=None)
        register_cache("serialization", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_5() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache(None, _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_6() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("serialization", None)
    return _serialization_cache


def x_get_serialization_cache__mutmut_7() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache(_serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_8() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache(
            "serialization",
        )
    return _serialization_cache


def x_get_serialization_cache__mutmut_9() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("XXserializationXX", _serialization_cache)
    return _serialization_cache


def x_get_serialization_cache__mutmut_10() -> LRUCache:
    """Get or create serialization cache with lazy initialization."""
    global _serialization_cache
    if _serialization_cache is None:
        from provide.foundation.utils.caching import LRUCache, register_cache

        config = _get_cache_config()
        _serialization_cache = LRUCache(maxsize=config.cache_size)
        register_cache("SERIALIZATION", _serialization_cache)
    return _serialization_cache


x_get_serialization_cache__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_serialization_cache__mutmut_1": x_get_serialization_cache__mutmut_1,
    "x_get_serialization_cache__mutmut_2": x_get_serialization_cache__mutmut_2,
    "x_get_serialization_cache__mutmut_3": x_get_serialization_cache__mutmut_3,
    "x_get_serialization_cache__mutmut_4": x_get_serialization_cache__mutmut_4,
    "x_get_serialization_cache__mutmut_5": x_get_serialization_cache__mutmut_5,
    "x_get_serialization_cache__mutmut_6": x_get_serialization_cache__mutmut_6,
    "x_get_serialization_cache__mutmut_7": x_get_serialization_cache__mutmut_7,
    "x_get_serialization_cache__mutmut_8": x_get_serialization_cache__mutmut_8,
    "x_get_serialization_cache__mutmut_9": x_get_serialization_cache__mutmut_9,
    "x_get_serialization_cache__mutmut_10": x_get_serialization_cache__mutmut_10,
}


def get_serialization_cache(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_serialization_cache__mutmut_orig, x_get_serialization_cache__mutmut_mutants, args, kwargs
    )
    return result


get_serialization_cache.__signature__ = _mutmut_signature(x_get_serialization_cache__mutmut_orig)
x_get_serialization_cache__mutmut_orig.__name__ = "x_get_serialization_cache"


def x_reset_serialization_cache_config__mutmut_orig() -> None:
    """Reset cached config for testing purposes."""
    global _cached_config, _serialization_cache
    _cached_config = None
    _serialization_cache = None


def x_reset_serialization_cache_config__mutmut_1() -> None:
    """Reset cached config for testing purposes."""
    global _cached_config, _serialization_cache
    _cached_config = ""
    _serialization_cache = None


def x_reset_serialization_cache_config__mutmut_2() -> None:
    """Reset cached config for testing purposes."""
    global _cached_config, _serialization_cache
    _cached_config = None
    _serialization_cache = ""


x_reset_serialization_cache_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_serialization_cache_config__mutmut_1": x_reset_serialization_cache_config__mutmut_1,
    "x_reset_serialization_cache_config__mutmut_2": x_reset_serialization_cache_config__mutmut_2,
}


def reset_serialization_cache_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_serialization_cache_config__mutmut_orig,
        x_reset_serialization_cache_config__mutmut_mutants,
        args,
        kwargs,
    )
    return result


reset_serialization_cache_config.__signature__ = _mutmut_signature(
    x_reset_serialization_cache_config__mutmut_orig
)
x_reset_serialization_cache_config__mutmut_orig.__name__ = "x_reset_serialization_cache_config"


# Convenience constants - use functions for actual access
CACHE_ENABLED = get_cache_enabled
CACHE_SIZE = get_cache_size
serialization_cache = get_serialization_cache


def x_get_cache_key__mutmut_orig(content: str, format: str) -> str:
    """Generate cache key from content and format.

    Args:
        content: String content to hash
        format: Format identifier (json, yaml, toml, etc.)

    Returns:
        Cache key string

    """
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"{format}:{content_hash}"


def x_get_cache_key__mutmut_1(content: str, format: str) -> str:
    """Generate cache key from content and format.

    Args:
        content: String content to hash
        format: Format identifier (json, yaml, toml, etc.)

    Returns:
        Cache key string

    """
    content_hash = None
    return f"{format}:{content_hash}"


def x_get_cache_key__mutmut_2(content: str, format: str) -> str:
    """Generate cache key from content and format.

    Args:
        content: String content to hash
        format: Format identifier (json, yaml, toml, etc.)

    Returns:
        Cache key string

    """
    content_hash = hashlib.sha256(None).hexdigest()[:16]
    return f"{format}:{content_hash}"


def x_get_cache_key__mutmut_3(content: str, format: str) -> str:
    """Generate cache key from content and format.

    Args:
        content: String content to hash
        format: Format identifier (json, yaml, toml, etc.)

    Returns:
        Cache key string

    """
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:17]
    return f"{format}:{content_hash}"


x_get_cache_key__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_cache_key__mutmut_1": x_get_cache_key__mutmut_1,
    "x_get_cache_key__mutmut_2": x_get_cache_key__mutmut_2,
    "x_get_cache_key__mutmut_3": x_get_cache_key__mutmut_3,
}


def get_cache_key(*args, **kwargs):
    result = _mutmut_trampoline(x_get_cache_key__mutmut_orig, x_get_cache_key__mutmut_mutants, args, kwargs)
    return result


get_cache_key.__signature__ = _mutmut_signature(x_get_cache_key__mutmut_orig)
x_get_cache_key__mutmut_orig.__name__ = "x_get_cache_key"


__all__ = [
    "CACHE_ENABLED",
    "CACHE_SIZE",
    "get_cache_key",
    "serialization_cache",
]


# <3 🧱🤝📜🪄
