#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import platform

from provide.foundation.logger import get_logger
from provide.foundation.utils.caching import cached

"""Detailed CPU information utilities.

Provides detailed CPU information including flags, features, brand names,
and architecture details.

Requires the optional 'py-cpuinfo' package for detailed information.
Falls back to stdlib platform module when not available.
Install with: pip install provide-foundation[platform]
"""

log = get_logger(__name__)

# Try to import py-cpuinfo
try:
    import cpuinfo  # type: ignore[import-untyped]

    _HAS_CPUINFO = True
except ImportError:
    _HAS_CPUINFO = False
    log.debug(
        "py-cpuinfo not available, using basic CPU info from platform module",
        hint="For detailed CPU info, install with: pip install provide-foundation[platform]",
    )


@cached()
def get_cpu_info() -> dict[str, str | int | list[str] | None]:
    """Get detailed CPU information.

    Returns comprehensive CPU information including brand, vendor, architecture,
    flags, and feature support.

    Returns:
        Dictionary containing CPU information. Keys include:
        - brand: CPU brand string (e.g., "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz")
        - vendor_id: Vendor identifier (e.g., "GenuineIntel", "AuthenticAMD")
        - arch: Architecture (e.g., "X86_64", "ARM_8")
        - bits: Bit width (32 or 64)
        - count: Number of logical CPUs
        - flags: List of CPU flags/features (e.g., ["sse", "avx", "avx2"])
        - hz_advertised: Advertised clock speed in Hz
        - hz_actual: Actual clock speed in Hz
        - family: CPU family
        - model: CPU model
        - stepping: CPU stepping

        When py-cpuinfo is not available, returns basic information from
        platform module.

    Example:
        >>> from provide.foundation.platform import get_cpu_info
        >>> info = get_cpu_info()
        >>> info['brand']
        'Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz'
        >>> 'avx2' in info.get('flags', [])
        True

    """
    if _HAS_CPUINFO:
        try:
            info = cpuinfo.get_cpu_info()
            log.debug(
                "Detailed CPU info gathered",
                brand=info.get("brand_raw"),
                arch=info.get("arch"),
                count=info.get("count"),
            )
            return info
        except Exception as e:
            log.warning("Failed to get detailed CPU info, falling back to basic info", error=str(e))

    # Fallback: Basic CPU info from platform module
    basic_info: dict[str, str | int | list[str] | None] = {
        "brand": platform.processor() or "Unknown",
        "vendor_id": None,
        "arch": platform.machine(),
        "bits": 64 if platform.machine().endswith("64") else 32,
        "count": None,
        "flags": None,
        "hz_advertised": None,
        "hz_actual": None,
        "family": None,
        "model": None,
        "stepping": None,
    }

    # Try to get CPU count from os module
    try:
        import os

        basic_info["count"] = os.cpu_count()
    except Exception:
        pass

    log.debug("Basic CPU info gathered (py-cpuinfo not available)", arch=basic_info["arch"])

    return basic_info


def get_cpu_brand() -> str:
    """Get CPU brand string.

    Returns:
        CPU brand string (e.g., "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz")

    Example:
        >>> from provide.foundation.platform import get_cpu_brand
        >>> get_cpu_brand()
        'Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz'

    """
    info = get_cpu_info()
    return str(info.get("brand_raw") or info.get("brand") or "Unknown")


def get_cpu_flags() -> list[str]:
    """Get list of CPU flags/features.

    Returns:
        List of CPU flags (e.g., ["sse", "avx", "avx2"]), or empty list if not available

    Example:
        >>> from provide.foundation.platform import get_cpu_flags
        >>> flags = get_cpu_flags()
        >>> 'avx2' in flags
        True

    """
    info = get_cpu_info()
    flags = info.get("flags")
    if flags is None:
        return []
    if isinstance(flags, list):
        return flags
    return []


def has_cpu_flag(flag: str) -> bool:
    """Check if CPU has a specific flag/feature.

    Args:
        flag: Flag name to check (e.g., "avx2", "sse4_2")

    Returns:
        True if CPU has the flag, False otherwise

    Example:
        >>> from provide.foundation.platform import has_cpu_flag
        >>> has_cpu_flag('avx2')
        True
        >>> has_cpu_flag('avx512f')
        False

    """
    return flag.lower() in [f.lower() for f in get_cpu_flags()]


def get_cpu_count() -> int | None:
    """Get number of logical CPUs.

    Returns:
        Number of logical CPUs, or None if not available

    Example:
        >>> from provide.foundation.platform import get_cpu_count
        >>> get_cpu_count()
        8

    """
    info = get_cpu_info()
    count = info.get("count")
    if count is None:
        return None
    return int(count)


def has_cpuinfo() -> bool:
    """Check if py-cpuinfo is available.

    Returns:
        True if py-cpuinfo is available, False otherwise

    Example:
        >>> from provide.foundation.platform import has_cpuinfo
        >>> if has_cpuinfo():
        ...     # Use detailed CPU features
        ...     pass

    """
    return _HAS_CPUINFO


__all__ = [
    "get_cpu_brand",
    "get_cpu_count",
    "get_cpu_flags",
    "get_cpu_info",
    "has_cpu_flag",
    "has_cpuinfo",
]

# 🧱🏗️🔚
