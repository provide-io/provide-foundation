#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


class CacheError(FoundationError):
    """Raised when cache operations fail."""


class ToolCache:
    """Cache for installed tools with TTL support.

    Tracks installed tool locations and expiration times to
    avoid unnecessary re-downloads and installations.
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache.

        Args:
            cache_dir: Cache directory (defaults to ~/.provide-foundation/cache).

        """
        self.cache_dir = cache_dir or (Path.home() / ".provide-foundation" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict[str, dict]:
        """Load cache metadata from disk.

        Returns:
            Cache metadata dictionary.

        """
        return read_json(self.metadata_file, default={})

    def _save_metadata(self) -> None:
        """Save cache metadata to disk."""
        try:
            write_json(self.metadata_file, self.metadata, indent=2)
        except Exception as e:
            log.error(f"Failed to save cache metadata: {e}")
            raise

    def get(self, tool: str, version: str) -> Path | None:
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

    def store(self, tool: str, version: str, path: Path, ttl_days: int = 7) -> None:
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

    def invalidate(self, tool: str, version: str | None = None) -> None:
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

    def _is_expired(self, entry: dict) -> bool:
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

    def clear(self) -> None:
        """Clear all cache entries."""
        self.metadata = {}
        self._save_metadata()
        log.info("Cleared tool cache")

    def list_cached(self) -> list[dict]:
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

    def get_size(self) -> int:
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

    def prune_expired(self) -> int:
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


# 🧱🏗️🔚
