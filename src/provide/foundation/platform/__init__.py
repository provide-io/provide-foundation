#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.platform.cpu import (
    get_cpu_brand,
    get_cpu_count,
    get_cpu_flags,
    get_cpu_info,
    has_cpu_flag,
    has_cpuinfo,
)
from provide.foundation.platform.detection import (
    PlatformError,
    get_arch_name,
    get_cpu_type,
    get_os_name,
    get_os_version,
    get_platform_string,
    normalize_platform_components,
)
from provide.foundation.platform.info import (
    SystemInfo,
    get_system_info,
    is_64bit,
    is_arm,
    is_linux,
    is_macos,
    is_windows,
)
from provide.foundation.platform.systemd import (
    has_systemd,
    notify_error,
    notify_ready,
    notify_reloading,
    notify_status,
    notify_stopping,
    notify_watchdog,
)

"""Platform detection and information utilities.

Provides cross-platform detection, system information gathering, detailed
CPU information, and systemd integration (Linux).
"""

__all__ = [
    # Classes
    "PlatformError",
    "SystemInfo",
    # Detection functions
    "get_arch_name",
    # CPU information (optional: py-cpuinfo)
    "get_cpu_brand",
    "get_cpu_count",
    "get_cpu_flags",
    "get_cpu_info",
    "get_cpu_type",
    "get_os_name",
    "get_os_version",
    "get_platform_string",
    "get_system_info",
    "has_cpu_flag",
    "has_cpuinfo",
    # systemd integration (optional: sdnotify, Linux only)
    "has_systemd",
    # Platform checks
    "is_64bit",
    "is_arm",
    "is_linux",
    "is_macos",
    "is_windows",
    # Utilities
    "normalize_platform_components",
    "notify_error",
    "notify_ready",
    "notify_reloading",
    "notify_status",
    "notify_stopping",
    "notify_watchdog",
]

# 🧱🏗️🔚
