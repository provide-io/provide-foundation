#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import platform
import re

from provide.foundation.errors.platform import PlatformError
from provide.foundation.logger import get_logger
from provide.foundation.utils.caching import cached

"""Core platform detection functions."""

log = get_logger(__name__)


@cached()
def get_os_name() -> str:
    """Get normalized OS name.

    Returns:
        Normalized OS name (darwin, linux, windows)

    """
    try:
        os_name = platform.system().lower()
        if os_name in ("darwin", "macos"):
            return "darwin"
        return os_name
    except Exception as e:
        log.error("Failed to detect OS", error=str(e))
        raise PlatformError(
            "Failed to detect operating system",
            code="PLATFORM_OS_DETECTION_FAILED",
            error=str(e),
        ) from e


@cached()
def get_arch_name() -> str:
    """Get normalized architecture name.

    Returns:
        Normalized architecture (amd64, arm64, x86, i386)

    """
    try:
        arch = platform.machine().lower()
        # Normalize common architectures
        if arch in ["x86_64", "amd64"]:
            return "amd64"
        if arch in ["aarch64", "arm64"]:
            return "arm64"
        if arch in ["i686", "i586", "i486"]:
            return "x86"
        return arch
    except Exception as e:
        log.error("Failed to detect architecture", error=str(e))
        raise PlatformError(
            "Failed to detect architecture",
            code="PLATFORM_ARCH_DETECTION_FAILED",
            error=str(e),
        ) from e


@cached()
def get_platform_string() -> str:
    """Get normalized platform string in format 'os_arch'.

    Returns:
        Platform string like 'darwin_arm64' or 'linux_amd64'

    """
    os_name = get_os_name()
    arch = get_arch_name()
    platform_str = f"{os_name}_{arch}"
    log.debug("Detected platform", platform=platform_str, os=os_name, arch=arch)
    return platform_str


@cached()
def get_os_version() -> str | None:
    """Get OS version information.

    Returns:
        OS version string or None if unavailable

    """
    try:
        system = platform.system()

        if system == "Darwin":
            # macOS version
            mac_ver = platform.mac_ver()
            if mac_ver[0]:
                return mac_ver[0]
        elif system == "Linux":
            # Linux kernel version
            release = platform.release()
            if release:
                # Extract major.minor version
                parts = release.split(".")
                if len(parts) >= 2:
                    return f"{parts[0]}.{parts[1]}"
                return release
        elif system == "Windows":
            # Windows version
            version = platform.version()
            if version:
                return version

        # Fallback to platform.release()
        release = platform.release()
        if release:
            return release
    except Exception as e:
        log.warning("Failed to detect OS version", error=str(e))

    return None


def _detect_intel_cpu(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def _detect_amd_cpu(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def _detect_apple_cpu(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


@cached()
def get_cpu_type() -> str | None:
    """Get CPU type/family information.

    Returns:
        CPU type string or None if unavailable

    """
    try:
        processor = platform.processor()
        if not processor:
            return None

        # Try different CPU detection strategies
        for detector in [_detect_intel_cpu, _detect_amd_cpu, _detect_apple_cpu]:
            result = detector(processor)
            if result:
                return result

        # Return cleaned processor string as fallback
        return processor.strip()

    except Exception as e:
        log.warning("Failed to detect CPU type", error=str(e))

    return None


def normalize_platform_components(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = {
        "linux": "linux",
        "darwin": "darwin",
        "macos": "darwin",
        "windows": "windows",
        "win32": "windows",
    }

    # Normalize architecture names
    arch_map = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


# 🧱🏗️🔚
