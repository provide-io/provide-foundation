# provide/foundation/platform/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

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

"""Platform detection and information utilities.

Provides cross-platform detection and system information gathering.
"""

__all__ = [
    # Classes
    "PlatformError",
    "SystemInfo",
    # Detection functions
    "get_arch_name",
    "get_cpu_type",
    "get_os_name",
    "get_os_version",
    "get_platform_string",
    "get_system_info",
    # Platform checks
    "is_64bit",
    "is_arm",
    "is_linux",
    "is_macos",
    "is_windows",
    # Utilities
    "normalize_platform_components",
]


# <3 🧱🤝🏗️🪄
