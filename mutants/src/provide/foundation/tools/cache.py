# provide/foundation/tools/cache.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.foundation.errors import FoundationError
from provide.foundation.file.formats import read_json, write_json
from provide.foundation.logger import get_logger

"""Caching system for installed tools.

Provides TTL-based caching to avoid re-downloading tools
that are already installed and valid.
"""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class CacheError(FoundationError):
    """Raised when cache operations fail."""


class ToolCache:
    """Cache for installed tools with TTL support.

    Tracks installed tool locations and expiration times to
    avoid unnecessary re-downloads and installations.
    """

    def xǁToolCacheǁ__init____mutmut_orig(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_1(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = None
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_2(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir and (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_3(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" * "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_4(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() * ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_5(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / "XX.provide-foundationXX" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_6(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".PROVIDE-FOUNDATION" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_7(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "XXcacheXX")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_8(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "CACHE")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_9(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=None, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_10(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=None)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_11(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_12(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, )

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_13(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=False, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_14(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=False)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_15(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = None
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_16(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir * "metadata.json"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_17(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "XXmetadata.jsonXX"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_18(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "METADATA.JSON"
        self.metadata = self._load_metadata()

    def xǁToolCacheǁ__init____mutmut_19(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = None
    
    xǁToolCacheǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁ__init____mutmut_1': xǁToolCacheǁ__init____mutmut_1, 
        'xǁToolCacheǁ__init____mutmut_2': xǁToolCacheǁ__init____mutmut_2, 
        'xǁToolCacheǁ__init____mutmut_3': xǁToolCacheǁ__init____mutmut_3, 
        'xǁToolCacheǁ__init____mutmut_4': xǁToolCacheǁ__init____mutmut_4, 
        'xǁToolCacheǁ__init____mutmut_5': xǁToolCacheǁ__init____mutmut_5, 
        'xǁToolCacheǁ__init____mutmut_6': xǁToolCacheǁ__init____mutmut_6, 
        'xǁToolCacheǁ__init____mutmut_7': xǁToolCacheǁ__init____mutmut_7, 
        'xǁToolCacheǁ__init____mutmut_8': xǁToolCacheǁ__init____mutmut_8, 
        'xǁToolCacheǁ__init____mutmut_9': xǁToolCacheǁ__init____mutmut_9, 
        'xǁToolCacheǁ__init____mutmut_10': xǁToolCacheǁ__init____mutmut_10, 
        'xǁToolCacheǁ__init____mutmut_11': xǁToolCacheǁ__init____mutmut_11, 
        'xǁToolCacheǁ__init____mutmut_12': xǁToolCacheǁ__init____mutmut_12, 
        'xǁToolCacheǁ__init____mutmut_13': xǁToolCacheǁ__init____mutmut_13, 
        'xǁToolCacheǁ__init____mutmut_14': xǁToolCacheǁ__init____mutmut_14, 
        'xǁToolCacheǁ__init____mutmut_15': xǁToolCacheǁ__init____mutmut_15, 
        'xǁToolCacheǁ__init____mutmut_16': xǁToolCacheǁ__init____mutmut_16, 
        'xǁToolCacheǁ__init____mutmut_17': xǁToolCacheǁ__init____mutmut_17, 
        'xǁToolCacheǁ__init____mutmut_18': xǁToolCacheǁ__init____mutmut_18, 
        'xǁToolCacheǁ__init____mutmut_19': xǁToolCacheǁ__init____mutmut_19
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁToolCacheǁ__init____mutmut_orig)
    xǁToolCacheǁ__init____mutmut_orig.__name__ = 'xǁToolCacheǁ__init__'

    def xǁToolCacheǁ_load_metadata__mutmut_orig(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(self.metadata_file, default={})

    def xǁToolCacheǁ_load_metadata__mutmut_1(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(None, default={})

    def xǁToolCacheǁ_load_metadata__mutmut_2(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(self.metadata_file, default=None)

    def xǁToolCacheǁ_load_metadata__mutmut_3(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(default={})

    def xǁToolCacheǁ_load_metadata__mutmut_4(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(self.metadata_file, )
    
    xǁToolCacheǁ_load_metadata__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁ_load_metadata__mutmut_1': xǁToolCacheǁ_load_metadata__mutmut_1, 
        'xǁToolCacheǁ_load_metadata__mutmut_2': xǁToolCacheǁ_load_metadata__mutmut_2, 
        'xǁToolCacheǁ_load_metadata__mutmut_3': xǁToolCacheǁ_load_metadata__mutmut_3, 
        'xǁToolCacheǁ_load_metadata__mutmut_4': xǁToolCacheǁ_load_metadata__mutmut_4
    }
    
    def _load_metadata(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁ_load_metadata__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁ_load_metadata__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _load_metadata.__signature__ = _mutmut_signature(xǁToolCacheǁ_load_metadata__mutmut_orig)
    xǁToolCacheǁ_load_metadata__mutmut_orig.__name__ = 'xǁToolCacheǁ_load_metadata'

    def xǁToolCacheǁ_save_metadata__mutmut_orig(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_1(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(None, self.metadata, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_2(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, None, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_3(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, indent=None)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_4(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_5(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_6(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, )
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_7(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, indent=3)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def xǁToolCacheǁ_save_metadata__mutmut_8(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, indent=2)
        except Exception as e:
            log.error(None)
            raise
    
    xǁToolCacheǁ_save_metadata__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁ_save_metadata__mutmut_1': xǁToolCacheǁ_save_metadata__mutmut_1, 
        'xǁToolCacheǁ_save_metadata__mutmut_2': xǁToolCacheǁ_save_metadata__mutmut_2, 
        'xǁToolCacheǁ_save_metadata__mutmut_3': xǁToolCacheǁ_save_metadata__mutmut_3, 
        'xǁToolCacheǁ_save_metadata__mutmut_4': xǁToolCacheǁ_save_metadata__mutmut_4, 
        'xǁToolCacheǁ_save_metadata__mutmut_5': xǁToolCacheǁ_save_metadata__mutmut_5, 
        'xǁToolCacheǁ_save_metadata__mutmut_6': xǁToolCacheǁ_save_metadata__mutmut_6, 
        'xǁToolCacheǁ_save_metadata__mutmut_7': xǁToolCacheǁ_save_metadata__mutmut_7, 
        'xǁToolCacheǁ_save_metadata__mutmut_8': xǁToolCacheǁ_save_metadata__mutmut_8
    }
    
    def _save_metadata(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁ_save_metadata__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁ_save_metadata__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _save_metadata.__signature__ = _mutmut_signature(xǁToolCacheǁ_save_metadata__mutmut_orig)
    xǁToolCacheǁ_save_metadata__mutmut_orig.__name__ = 'xǁToolCacheǁ_save_metadata'

    def xǁToolCacheǁget__mutmut_orig(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_1(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = None

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_2(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(None):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_3(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = None

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_4(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(None)

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_5(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["XXpathXX"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_6(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["PATH"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_7(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_8(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(None)
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_9(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(None, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_10(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, None)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_11(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_12(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, )
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_13(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(None):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_14(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(None)
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_15(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(None, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_16(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, None)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_17(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_18(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, )
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_19(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(None)
            return path

        log.debug(f"Cache miss: {key} not in cache")
        return None

    def xǁToolCacheǁget__mutmut_20(self, tool: str, version: str) -> Path | None:
        """Get cached tool path if valid.

        Args:
            tool: Tool name.
            version: Tool version.

        Returns:
            Path to cached tool if valid, None otherwise.

        """
        key = f"{tool}:{version}"

        if entry := self.metadata.get(key):
            path = Path(entry["path"])

            # Check if path exists
            if not path.exists():
                log.debug(f"Cache miss: {key} path doesn't exist")
                self.invalidate(tool, version)
                return None

            # Check if expired
            if self._is_expired(entry):
                log.debug(f"Cache miss: {key} expired")
                self.invalidate(tool, version)
                return None

            log.debug(f"Cache hit: {key}")
            return path

        log.debug(None)
        return None
    
    xǁToolCacheǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁget__mutmut_1': xǁToolCacheǁget__mutmut_1, 
        'xǁToolCacheǁget__mutmut_2': xǁToolCacheǁget__mutmut_2, 
        'xǁToolCacheǁget__mutmut_3': xǁToolCacheǁget__mutmut_3, 
        'xǁToolCacheǁget__mutmut_4': xǁToolCacheǁget__mutmut_4, 
        'xǁToolCacheǁget__mutmut_5': xǁToolCacheǁget__mutmut_5, 
        'xǁToolCacheǁget__mutmut_6': xǁToolCacheǁget__mutmut_6, 
        'xǁToolCacheǁget__mutmut_7': xǁToolCacheǁget__mutmut_7, 
        'xǁToolCacheǁget__mutmut_8': xǁToolCacheǁget__mutmut_8, 
        'xǁToolCacheǁget__mutmut_9': xǁToolCacheǁget__mutmut_9, 
        'xǁToolCacheǁget__mutmut_10': xǁToolCacheǁget__mutmut_10, 
        'xǁToolCacheǁget__mutmut_11': xǁToolCacheǁget__mutmut_11, 
        'xǁToolCacheǁget__mutmut_12': xǁToolCacheǁget__mutmut_12, 
        'xǁToolCacheǁget__mutmut_13': xǁToolCacheǁget__mutmut_13, 
        'xǁToolCacheǁget__mutmut_14': xǁToolCacheǁget__mutmut_14, 
        'xǁToolCacheǁget__mutmut_15': xǁToolCacheǁget__mutmut_15, 
        'xǁToolCacheǁget__mutmut_16': xǁToolCacheǁget__mutmut_16, 
        'xǁToolCacheǁget__mutmut_17': xǁToolCacheǁget__mutmut_17, 
        'xǁToolCacheǁget__mutmut_18': xǁToolCacheǁget__mutmut_18, 
        'xǁToolCacheǁget__mutmut_19': xǁToolCacheǁget__mutmut_19, 
        'xǁToolCacheǁget__mutmut_20': xǁToolCacheǁget__mutmut_20
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁget__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁToolCacheǁget__mutmut_orig)
    xǁToolCacheǁget__mutmut_orig.__name__ = 'xǁToolCacheǁget'

    def xǁToolCacheǁstore__mutmut_orig(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_1(self, tool: str, version: str, path: Path, ttl_days: int = 8) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_2(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = None

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_3(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = None

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_4(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "XXpathXX": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_5(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "PATH": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_6(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(None),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_7(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "XXtoolXX": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_8(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "TOOL": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_9(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "XXversionXX": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_10(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "VERSION": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_11(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "XXcached_atXX": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_12(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "CACHED_AT": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_13(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "XXttl_daysXX": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_14(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "TTL_DAYS": ttl_days,
        }

        self._save_metadata()
        log.debug(f"Cached {key} at {path} (TTL: {ttl_days} days)")

    def xǁToolCacheǁstore__mutmut_15(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
        """Store tool in cache.

        Args:
            tool: Tool name.
            version: Tool version.
            path: Path to installed tool.
            ttl_days: Time-to-live in days.

        """
        key = f"{tool}:{version}"

        self.metadata[key] = {
            "path": str(path),
            "tool": tool,
            "version": version,
            "cached_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
        }

        self._save_metadata()
        log.debug(None)
    
    xǁToolCacheǁstore__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁstore__mutmut_1': xǁToolCacheǁstore__mutmut_1, 
        'xǁToolCacheǁstore__mutmut_2': xǁToolCacheǁstore__mutmut_2, 
        'xǁToolCacheǁstore__mutmut_3': xǁToolCacheǁstore__mutmut_3, 
        'xǁToolCacheǁstore__mutmut_4': xǁToolCacheǁstore__mutmut_4, 
        'xǁToolCacheǁstore__mutmut_5': xǁToolCacheǁstore__mutmut_5, 
        'xǁToolCacheǁstore__mutmut_6': xǁToolCacheǁstore__mutmut_6, 
        'xǁToolCacheǁstore__mutmut_7': xǁToolCacheǁstore__mutmut_7, 
        'xǁToolCacheǁstore__mutmut_8': xǁToolCacheǁstore__mutmut_8, 
        'xǁToolCacheǁstore__mutmut_9': xǁToolCacheǁstore__mutmut_9, 
        'xǁToolCacheǁstore__mutmut_10': xǁToolCacheǁstore__mutmut_10, 
        'xǁToolCacheǁstore__mutmut_11': xǁToolCacheǁstore__mutmut_11, 
        'xǁToolCacheǁstore__mutmut_12': xǁToolCacheǁstore__mutmut_12, 
        'xǁToolCacheǁstore__mutmut_13': xǁToolCacheǁstore__mutmut_13, 
        'xǁToolCacheǁstore__mutmut_14': xǁToolCacheǁstore__mutmut_14, 
        'xǁToolCacheǁstore__mutmut_15': xǁToolCacheǁstore__mutmut_15
    }
    
    def store(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁstore__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁstore__mutmut_mutants"), args, kwargs, self)
        return result 
    
    store.__signature__ = _mutmut_signature(xǁToolCacheǁstore__mutmut_orig)
    xǁToolCacheǁstore__mutmut_orig.__name__ = 'xǁToolCacheǁstore'

    def xǁToolCacheǁinvalidate__mutmut_orig(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_1(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = None
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_2(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key not in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_3(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(None)
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_4(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = None
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_5(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get(None) == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_6(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("XXtoolXX") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_7(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("TOOL") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_8(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") != tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")

        self._save_metadata()

    def xǁToolCacheǁinvalidate__mutmut_9(self, tool: str, version: str | None = None) -> None:
        """Invalidate cache entries.

        Args:
            tool: Tool name.
            version: Specific version, or None for all versions.

        """
        if version:
            # Invalidate specific version
            key = f"{tool}:{version}"
            if key in self.metadata:
                del self.metadata[key]
                log.debug(f"Invalidated cache for {key}")
        else:
            # Invalidate all versions of tool
            keys_to_remove = [k for k in self.metadata if self.metadata[k].get("tool") == tool]
            for key in keys_to_remove:
                del self.metadata[key]
                log.debug(None)

        self._save_metadata()
    
    xǁToolCacheǁinvalidate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁinvalidate__mutmut_1': xǁToolCacheǁinvalidate__mutmut_1, 
        'xǁToolCacheǁinvalidate__mutmut_2': xǁToolCacheǁinvalidate__mutmut_2, 
        'xǁToolCacheǁinvalidate__mutmut_3': xǁToolCacheǁinvalidate__mutmut_3, 
        'xǁToolCacheǁinvalidate__mutmut_4': xǁToolCacheǁinvalidate__mutmut_4, 
        'xǁToolCacheǁinvalidate__mutmut_5': xǁToolCacheǁinvalidate__mutmut_5, 
        'xǁToolCacheǁinvalidate__mutmut_6': xǁToolCacheǁinvalidate__mutmut_6, 
        'xǁToolCacheǁinvalidate__mutmut_7': xǁToolCacheǁinvalidate__mutmut_7, 
        'xǁToolCacheǁinvalidate__mutmut_8': xǁToolCacheǁinvalidate__mutmut_8, 
        'xǁToolCacheǁinvalidate__mutmut_9': xǁToolCacheǁinvalidate__mutmut_9
    }
    
    def invalidate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁinvalidate__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁinvalidate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    invalidate.__signature__ = _mutmut_signature(xǁToolCacheǁinvalidate__mutmut_orig)
    xǁToolCacheǁinvalidate__mutmut_orig.__name__ = 'xǁToolCacheǁinvalidate'

    def xǁToolCacheǁ_is_expired__mutmut_orig(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_1(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = None
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_2(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(None)
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_3(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["XXcached_atXX"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_4(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["CACHED_AT"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_5(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = None

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_6(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get(None, 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_7(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", None)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_8(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get(7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_9(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", )

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_10(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("XXttl_daysXX", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_11(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("TTL_DAYS", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_12(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 8)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_13(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days < 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_14(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 1:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_15(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return True

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_16(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = None
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_17(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at - timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_18(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=None)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_19(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() >= expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_20(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(None)
            return True  # Treat as expired if we can't determine

    def xǁToolCacheǁ_is_expired__mutmut_21(self, entry: dict) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: Cache entry dictionary.

        Returns:
            True if expired, False otherwise.

        """
        try:
            cached_at = datetime.fromisoformat(entry["cached_at"])
            ttl_days = entry.get("ttl_days", 7)

            if ttl_days <= 0:
                # Never expires
                return False

            expiry = cached_at + timedelta(days=ttl_days)
            return datetime.now() > expiry
        except Exception as e:
            log.debug(f"Error checking expiry: {e}")
            return False  # Treat as expired if we can't determine
    
    xǁToolCacheǁ_is_expired__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁ_is_expired__mutmut_1': xǁToolCacheǁ_is_expired__mutmut_1, 
        'xǁToolCacheǁ_is_expired__mutmut_2': xǁToolCacheǁ_is_expired__mutmut_2, 
        'xǁToolCacheǁ_is_expired__mutmut_3': xǁToolCacheǁ_is_expired__mutmut_3, 
        'xǁToolCacheǁ_is_expired__mutmut_4': xǁToolCacheǁ_is_expired__mutmut_4, 
        'xǁToolCacheǁ_is_expired__mutmut_5': xǁToolCacheǁ_is_expired__mutmut_5, 
        'xǁToolCacheǁ_is_expired__mutmut_6': xǁToolCacheǁ_is_expired__mutmut_6, 
        'xǁToolCacheǁ_is_expired__mutmut_7': xǁToolCacheǁ_is_expired__mutmut_7, 
        'xǁToolCacheǁ_is_expired__mutmut_8': xǁToolCacheǁ_is_expired__mutmut_8, 
        'xǁToolCacheǁ_is_expired__mutmut_9': xǁToolCacheǁ_is_expired__mutmut_9, 
        'xǁToolCacheǁ_is_expired__mutmut_10': xǁToolCacheǁ_is_expired__mutmut_10, 
        'xǁToolCacheǁ_is_expired__mutmut_11': xǁToolCacheǁ_is_expired__mutmut_11, 
        'xǁToolCacheǁ_is_expired__mutmut_12': xǁToolCacheǁ_is_expired__mutmut_12, 
        'xǁToolCacheǁ_is_expired__mutmut_13': xǁToolCacheǁ_is_expired__mutmut_13, 
        'xǁToolCacheǁ_is_expired__mutmut_14': xǁToolCacheǁ_is_expired__mutmut_14, 
        'xǁToolCacheǁ_is_expired__mutmut_15': xǁToolCacheǁ_is_expired__mutmut_15, 
        'xǁToolCacheǁ_is_expired__mutmut_16': xǁToolCacheǁ_is_expired__mutmut_16, 
        'xǁToolCacheǁ_is_expired__mutmut_17': xǁToolCacheǁ_is_expired__mutmut_17, 
        'xǁToolCacheǁ_is_expired__mutmut_18': xǁToolCacheǁ_is_expired__mutmut_18, 
        'xǁToolCacheǁ_is_expired__mutmut_19': xǁToolCacheǁ_is_expired__mutmut_19, 
        'xǁToolCacheǁ_is_expired__mutmut_20': xǁToolCacheǁ_is_expired__mutmut_20, 
        'xǁToolCacheǁ_is_expired__mutmut_21': xǁToolCacheǁ_is_expired__mutmut_21
    }
    
    def _is_expired(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁ_is_expired__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁ_is_expired__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_expired.__signature__ = _mutmut_signature(xǁToolCacheǁ_is_expired__mutmut_orig)
    xǁToolCacheǁ_is_expired__mutmut_orig.__name__ = 'xǁToolCacheǁ_is_expired'

    def xǁToolCacheǁclear__mutmut_orig(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info("Cleared tool cache")

    def xǁToolCacheǁclear__mutmut_1(self) -> None:
        """Clear all cache entries."""
        self.metadata = None
        self._save_metadata()
        log.info("Cleared tool cache")

    def xǁToolCacheǁclear__mutmut_2(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info(None)

    def xǁToolCacheǁclear__mutmut_3(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info("XXCleared tool cacheXX")

    def xǁToolCacheǁclear__mutmut_4(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info("cleared tool cache")

    def xǁToolCacheǁclear__mutmut_5(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info("CLEARED TOOL CACHE")
    
    xǁToolCacheǁclear__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁclear__mutmut_1': xǁToolCacheǁclear__mutmut_1, 
        'xǁToolCacheǁclear__mutmut_2': xǁToolCacheǁclear__mutmut_2, 
        'xǁToolCacheǁclear__mutmut_3': xǁToolCacheǁclear__mutmut_3, 
        'xǁToolCacheǁclear__mutmut_4': xǁToolCacheǁclear__mutmut_4, 
        'xǁToolCacheǁclear__mutmut_5': xǁToolCacheǁclear__mutmut_5
    }
    
    def clear(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁclear__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁclear__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear.__signature__ = _mutmut_signature(xǁToolCacheǁclear__mutmut_orig)
    xǁToolCacheǁclear__mutmut_orig.__name__ = 'xǁToolCacheǁclear'

    def xǁToolCacheǁlist_cached__mutmut_orig(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_1(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = None

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_2(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = None
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_3(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = None
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_4(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["XXkeyXX"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_5(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["KEY"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_6(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = None

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_7(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["XXexpiredXX"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_8(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["EXPIRED"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_9(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(None)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_10(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = None
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_11(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(None)
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_12(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["XXcached_atXX"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_13(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["CACHED_AT"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_14(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = None
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_15(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get(None, 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_16(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", None)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_17(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get(7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_18(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", )
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_19(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("XXttl_daysXX", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_20(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("TTL_DAYS", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_21(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 8)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_22(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days >= 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_23(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 1:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_24(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = None
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_25(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at - timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_26(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=None)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_27(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = None
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_28(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry + datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_29(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = None
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_30(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["XXdays_until_expiryXX"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_31(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["DAYS_UNTIL_EXPIRY"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_32(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(None, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_33(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, None)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_34(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_35(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, )
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_36(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(1, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_37(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = None  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_38(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["XXdays_until_expiryXX"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_39(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["DAYS_UNTIL_EXPIRY"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_40(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = +1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_41(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -2  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_42(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = None

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_43(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["XXdays_until_expiryXX"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_44(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["DAYS_UNTIL_EXPIRY"] = 0

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_45(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 1

            results.append(entry)

        return results

    def xǁToolCacheǁlist_cached__mutmut_46(self) -> list[dict]:
        """List all cached tools.

        Returns:
            List of cache entries with metadata.

        """
        results = []

        for key, entry in self.metadata.items():
            # Add expiry status
            entry = entry.copy()
            entry["key"] = key
            entry["expired"] = self._is_expired(entry)

            # Calculate days until expiry
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                ttl_days = entry.get("ttl_days", 7)
                if ttl_days > 0:
                    expiry = cached_at + timedelta(days=ttl_days)
                    days_left = (expiry - datetime.now()).days
                    entry["days_until_expiry"] = max(0, days_left)
                else:
                    entry["days_until_expiry"] = -1  # Never expires
            except Exception:
                entry["days_until_expiry"] = 0

            results.append(None)

        return results
    
    xǁToolCacheǁlist_cached__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁlist_cached__mutmut_1': xǁToolCacheǁlist_cached__mutmut_1, 
        'xǁToolCacheǁlist_cached__mutmut_2': xǁToolCacheǁlist_cached__mutmut_2, 
        'xǁToolCacheǁlist_cached__mutmut_3': xǁToolCacheǁlist_cached__mutmut_3, 
        'xǁToolCacheǁlist_cached__mutmut_4': xǁToolCacheǁlist_cached__mutmut_4, 
        'xǁToolCacheǁlist_cached__mutmut_5': xǁToolCacheǁlist_cached__mutmut_5, 
        'xǁToolCacheǁlist_cached__mutmut_6': xǁToolCacheǁlist_cached__mutmut_6, 
        'xǁToolCacheǁlist_cached__mutmut_7': xǁToolCacheǁlist_cached__mutmut_7, 
        'xǁToolCacheǁlist_cached__mutmut_8': xǁToolCacheǁlist_cached__mutmut_8, 
        'xǁToolCacheǁlist_cached__mutmut_9': xǁToolCacheǁlist_cached__mutmut_9, 
        'xǁToolCacheǁlist_cached__mutmut_10': xǁToolCacheǁlist_cached__mutmut_10, 
        'xǁToolCacheǁlist_cached__mutmut_11': xǁToolCacheǁlist_cached__mutmut_11, 
        'xǁToolCacheǁlist_cached__mutmut_12': xǁToolCacheǁlist_cached__mutmut_12, 
        'xǁToolCacheǁlist_cached__mutmut_13': xǁToolCacheǁlist_cached__mutmut_13, 
        'xǁToolCacheǁlist_cached__mutmut_14': xǁToolCacheǁlist_cached__mutmut_14, 
        'xǁToolCacheǁlist_cached__mutmut_15': xǁToolCacheǁlist_cached__mutmut_15, 
        'xǁToolCacheǁlist_cached__mutmut_16': xǁToolCacheǁlist_cached__mutmut_16, 
        'xǁToolCacheǁlist_cached__mutmut_17': xǁToolCacheǁlist_cached__mutmut_17, 
        'xǁToolCacheǁlist_cached__mutmut_18': xǁToolCacheǁlist_cached__mutmut_18, 
        'xǁToolCacheǁlist_cached__mutmut_19': xǁToolCacheǁlist_cached__mutmut_19, 
        'xǁToolCacheǁlist_cached__mutmut_20': xǁToolCacheǁlist_cached__mutmut_20, 
        'xǁToolCacheǁlist_cached__mutmut_21': xǁToolCacheǁlist_cached__mutmut_21, 
        'xǁToolCacheǁlist_cached__mutmut_22': xǁToolCacheǁlist_cached__mutmut_22, 
        'xǁToolCacheǁlist_cached__mutmut_23': xǁToolCacheǁlist_cached__mutmut_23, 
        'xǁToolCacheǁlist_cached__mutmut_24': xǁToolCacheǁlist_cached__mutmut_24, 
        'xǁToolCacheǁlist_cached__mutmut_25': xǁToolCacheǁlist_cached__mutmut_25, 
        'xǁToolCacheǁlist_cached__mutmut_26': xǁToolCacheǁlist_cached__mutmut_26, 
        'xǁToolCacheǁlist_cached__mutmut_27': xǁToolCacheǁlist_cached__mutmut_27, 
        'xǁToolCacheǁlist_cached__mutmut_28': xǁToolCacheǁlist_cached__mutmut_28, 
        'xǁToolCacheǁlist_cached__mutmut_29': xǁToolCacheǁlist_cached__mutmut_29, 
        'xǁToolCacheǁlist_cached__mutmut_30': xǁToolCacheǁlist_cached__mutmut_30, 
        'xǁToolCacheǁlist_cached__mutmut_31': xǁToolCacheǁlist_cached__mutmut_31, 
        'xǁToolCacheǁlist_cached__mutmut_32': xǁToolCacheǁlist_cached__mutmut_32, 
        'xǁToolCacheǁlist_cached__mutmut_33': xǁToolCacheǁlist_cached__mutmut_33, 
        'xǁToolCacheǁlist_cached__mutmut_34': xǁToolCacheǁlist_cached__mutmut_34, 
        'xǁToolCacheǁlist_cached__mutmut_35': xǁToolCacheǁlist_cached__mutmut_35, 
        'xǁToolCacheǁlist_cached__mutmut_36': xǁToolCacheǁlist_cached__mutmut_36, 
        'xǁToolCacheǁlist_cached__mutmut_37': xǁToolCacheǁlist_cached__mutmut_37, 
        'xǁToolCacheǁlist_cached__mutmut_38': xǁToolCacheǁlist_cached__mutmut_38, 
        'xǁToolCacheǁlist_cached__mutmut_39': xǁToolCacheǁlist_cached__mutmut_39, 
        'xǁToolCacheǁlist_cached__mutmut_40': xǁToolCacheǁlist_cached__mutmut_40, 
        'xǁToolCacheǁlist_cached__mutmut_41': xǁToolCacheǁlist_cached__mutmut_41, 
        'xǁToolCacheǁlist_cached__mutmut_42': xǁToolCacheǁlist_cached__mutmut_42, 
        'xǁToolCacheǁlist_cached__mutmut_43': xǁToolCacheǁlist_cached__mutmut_43, 
        'xǁToolCacheǁlist_cached__mutmut_44': xǁToolCacheǁlist_cached__mutmut_44, 
        'xǁToolCacheǁlist_cached__mutmut_45': xǁToolCacheǁlist_cached__mutmut_45, 
        'xǁToolCacheǁlist_cached__mutmut_46': xǁToolCacheǁlist_cached__mutmut_46
    }
    
    def list_cached(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁlist_cached__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁlist_cached__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_cached.__signature__ = _mutmut_signature(xǁToolCacheǁlist_cached__mutmut_orig)
    xǁToolCacheǁlist_cached__mutmut_orig.__name__ = 'xǁToolCacheǁlist_cached'

    def xǁToolCacheǁget_size__mutmut_orig(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_1(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = None

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_2(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 1

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_3(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = None
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_4(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(None)
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_5(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["XXpathXX"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_6(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["PATH"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_7(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob(None):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_8(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("XX*XX"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_9(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total = f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_10(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total -= f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_11(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(None)
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_12(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total = path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_13(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total -= path.stat().st_size
            except Exception as e:
                log.debug(f"Failed to get size of {path}: {e}")

        return total

    def xǁToolCacheǁget_size__mutmut_14(self) -> int:
        """Get total size of cached tools in bytes.

        Returns:
            Total size in bytes.

        """
        total = 0

        for entry in self.metadata.values():
            path = Path(entry["path"])
            try:
                if path.exists():
                    # Calculate directory size
                    if path.is_dir():
                        for f in path.rglob("*"):
                            if f.is_file():
                                try:
                                    total += f.stat().st_size
                                except Exception as e:
                                    log.debug(f"Failed to get size of file {f}: {e}")
                    else:
                        total += path.stat().st_size
            except Exception as e:
                log.debug(None)

        return total
    
    xǁToolCacheǁget_size__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁget_size__mutmut_1': xǁToolCacheǁget_size__mutmut_1, 
        'xǁToolCacheǁget_size__mutmut_2': xǁToolCacheǁget_size__mutmut_2, 
        'xǁToolCacheǁget_size__mutmut_3': xǁToolCacheǁget_size__mutmut_3, 
        'xǁToolCacheǁget_size__mutmut_4': xǁToolCacheǁget_size__mutmut_4, 
        'xǁToolCacheǁget_size__mutmut_5': xǁToolCacheǁget_size__mutmut_5, 
        'xǁToolCacheǁget_size__mutmut_6': xǁToolCacheǁget_size__mutmut_6, 
        'xǁToolCacheǁget_size__mutmut_7': xǁToolCacheǁget_size__mutmut_7, 
        'xǁToolCacheǁget_size__mutmut_8': xǁToolCacheǁget_size__mutmut_8, 
        'xǁToolCacheǁget_size__mutmut_9': xǁToolCacheǁget_size__mutmut_9, 
        'xǁToolCacheǁget_size__mutmut_10': xǁToolCacheǁget_size__mutmut_10, 
        'xǁToolCacheǁget_size__mutmut_11': xǁToolCacheǁget_size__mutmut_11, 
        'xǁToolCacheǁget_size__mutmut_12': xǁToolCacheǁget_size__mutmut_12, 
        'xǁToolCacheǁget_size__mutmut_13': xǁToolCacheǁget_size__mutmut_13, 
        'xǁToolCacheǁget_size__mutmut_14': xǁToolCacheǁget_size__mutmut_14
    }
    
    def get_size(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁget_size__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁget_size__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_size.__signature__ = _mutmut_signature(xǁToolCacheǁget_size__mutmut_orig)
    xǁToolCacheǁget_size__mutmut_orig.__name__ = 'xǁToolCacheǁget_size'

    def xǁToolCacheǁprune_expired__mutmut_orig(self) -> int:
        """Remove expired entries from cache.

        Returns:
            Number of entries removed.

        """
        expired_keys = [key for key, entry in self.metadata.items() if self._is_expired(entry)]

        for key in expired_keys:
            del self.metadata[key]

        if expired_keys:
            self._save_metadata()
            log.info(f"Pruned {len(expired_keys)} expired cache entries")

        return len(expired_keys)

    def xǁToolCacheǁprune_expired__mutmut_1(self) -> int:
        """Remove expired entries from cache.

        Returns:
            Number of entries removed.

        """
        expired_keys = None

        for key in expired_keys:
            del self.metadata[key]

        if expired_keys:
            self._save_metadata()
            log.info(f"Pruned {len(expired_keys)} expired cache entries")

        return len(expired_keys)

    def xǁToolCacheǁprune_expired__mutmut_2(self) -> int:
        """Remove expired entries from cache.

        Returns:
            Number of entries removed.

        """
        expired_keys = [key for key, entry in self.metadata.items() if self._is_expired(None)]

        for key in expired_keys:
            del self.metadata[key]

        if expired_keys:
            self._save_metadata()
            log.info(f"Pruned {len(expired_keys)} expired cache entries")

        return len(expired_keys)

    def xǁToolCacheǁprune_expired__mutmut_3(self) -> int:
        """Remove expired entries from cache.

        Returns:
            Number of entries removed.

        """
        expired_keys = [key for key, entry in self.metadata.items() if self._is_expired(entry)]

        for key in expired_keys:
            del self.metadata[key]

        if expired_keys:
            self._save_metadata()
            log.info(None)

        return len(expired_keys)
    
    xǁToolCacheǁprune_expired__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCacheǁprune_expired__mutmut_1': xǁToolCacheǁprune_expired__mutmut_1, 
        'xǁToolCacheǁprune_expired__mutmut_2': xǁToolCacheǁprune_expired__mutmut_2, 
        'xǁToolCacheǁprune_expired__mutmut_3': xǁToolCacheǁprune_expired__mutmut_3
    }
    
    def prune_expired(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCacheǁprune_expired__mutmut_orig"), object.__getattribute__(self, "xǁToolCacheǁprune_expired__mutmut_mutants"), args, kwargs, self)
        return result 
    
    prune_expired.__signature__ = _mutmut_signature(xǁToolCacheǁprune_expired__mutmut_orig)
    xǁToolCacheǁprune_expired__mutmut_orig.__name__ = 'xǁToolCacheǁprune_expired'


# <3 🧱🤝🔧🪄
