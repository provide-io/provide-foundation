"""Platform detection and system information utilities."""

from provide.foundation.platform.detection import (
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
)

__all__ = [
    "get_os_name",
    "get_arch_name",
    "get_platform_string",
    "get_os_version",
    "get_cpu_type",
    "normalize_platform_components",
    "SystemInfo",
    "get_system_info",
]