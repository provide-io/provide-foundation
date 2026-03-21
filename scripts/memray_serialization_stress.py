#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memray stress test: Serialization and caching.

Exercises JSON serialization (20K encode/decode cycles) and
LRUCache stress (10K cache hit/miss/eviction cycles).
"""

from __future__ import annotations

import sys


def warmup() -> None:
    """Warmup phase to separate import-time allocations."""
    from provide.foundation.serialization import json_dumps, json_loads
    from provide.foundation.utils.caching import LRUCache

    cache = LRUCache(maxsize=16)
    for i in range(20):
        cache.set(f"key_{i}", f"value_{i}")
        cache.get(f"key_{i}")

    data = {"warmup": True, "count": 1}
    json_loads(json_dumps(data))


def run_stress() -> None:
    """Run the serialization stress test."""
    from provide.foundation.serialization import json_dumps, json_loads
    from provide.foundation.utils.caching import LRUCache

    # Phase 1: JSON serialization — 20K encode/decode cycles with large payloads
    encode_decode_count = 20_000
    large_payload = {
        "users": [
            {
                "id": i,
                "name": f"user_{i}",
                "email": f"user_{i}@example.com",
                "settings": {
                    "theme": "dark",
                    "notifications": True,
                    "tags": [f"tag_{j}" for j in range(5)],
                },
            }
            for i in range(10)
        ],
        "metadata": {
            "version": "1.0",
            "generated": "2025-01-01T00:00:00Z",
            "counts": list(range(50)),
        },
    }

    for i in range(encode_decode_count):
        serialized = json_dumps(large_payload)
        json_loads(serialized)

    # Phase 2: LRUCache stress — 10K hit/miss/eviction cycles
    cache_ops = 10_000
    cache = LRUCache(maxsize=256)

    # Fill cache to capacity
    for i in range(256):
        cache.set(f"key_{i}", {"data": f"value_{i}", "index": i})

    # Mixed operations: hits, misses, and evictions
    for i in range(cache_ops):
        # Cache hit (existing key)
        cache.get(f"key_{i % 256}")

        # Cache miss (non-existent key)
        cache.get(f"miss_{i}")

        # Eviction (new key forces oldest out)
        cache.set(f"new_{i}", {"data": f"new_value_{i}", "index": i})

    stats = cache.stats()
    print(
        f"Serialization stress complete: {encode_decode_count} JSON cycles, "
        f"{cache_ops} cache ops (hit_rate: {stats['hit_rate']:.1f}%)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    warmup()
    run_stress()
