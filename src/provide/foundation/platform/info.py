"""System information gathering utilities."""

import contextlib
import os
import platform
import shutil
import sys

from attrs import define

from provide.foundation.logger import get_logger
from provide.foundation.platform.detection import (
    get_arch_name,
    get_cpu_type,
    get_os_name,
    get_os_version,
    get_platform_string,
)

plog = get_logger(__name__)


@define
class SystemInfo:
    """System information container."""

    os_name: str
    arch: str
    platform: str
    os_version: str | None
    cpu_type: str | None
    python_version: str
    hostname: str | None
    username: str | None
    home_dir: str | None
    temp_dir: str | None
    num_cpus: int | None
    total_memory: int | None
    available_memory: int | None
    disk_usage: dict[str, dict[str, int]] | None


def get_system_info() -> SystemInfo:
    """
    Gather comprehensive system information.

    Returns:
        SystemInfo object with all available system details
    """
    # Basic platform info
    os_name = get_os_name()
    arch = get_arch_name()
    platform_str = get_platform_string()
    os_version = get_os_version()
    cpu_type = get_cpu_type()

    # Python info
    python_version = platform.python_version()

    # System info
    hostname = None
    with contextlib.suppress(Exception):
        hostname = platform.node()

    # User info
    username = os.environ.get("USER") or os.environ.get("USERNAME")
    home_dir = os.path.expanduser("~")
    temp_dir = os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp"

    # CPU info
    num_cpus = None
    with contextlib.suppress(Exception):
        num_cpus = os.cpu_count()

    # Memory info (requires psutil for accurate values)
    total_memory = None
    available_memory = None
    try:
        import psutil

        mem = psutil.virtual_memory()
        total_memory = mem.total
        available_memory = mem.available
    except ImportError:
        plog.debug("psutil not available, memory info limited")
    except Exception as e:
        plog.debug("Failed to get memory info", error=str(e))

    # Disk usage
    disk_usage = None
    try:
        disk_usage = {}
        for path in ["/", home_dir, temp_dir]:
            if os.path.exists(path):
                usage = shutil.disk_usage(path)
                disk_usage[path] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                }
    except Exception as e:
        plog.debug("Failed to get disk usage", error=str(e))

    info = SystemInfo(
        os_name=os_name,
        arch=arch,
        platform=platform_str,
        os_version=os_version,
        cpu_type=cpu_type,
        python_version=python_version,
        hostname=hostname,
        username=username,
        home_dir=home_dir,
        temp_dir=temp_dir,
        num_cpus=num_cpus,
        total_memory=total_memory,
        available_memory=available_memory,
        disk_usage=disk_usage,
    )

    plog.debug(
        "System information gathered",
        platform=platform_str,
        os=os_name,
        arch=arch,
        python=python_version,
        cpus=num_cpus,
    )

    return info


# Platform detection functions
def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform.startswith("win")


def is_macos() -> bool:
    """Check if running on macOS."""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return sys.platform.startswith("linux")


def is_arm() -> bool:
    """Check if running on ARM architecture."""
    machine = platform.machine().lower()
    return "arm" in machine or "aarch" in machine


def is_64bit() -> bool:
    """Check if running on 64-bit architecture."""
    return platform.machine().endswith("64") or sys.maxsize > 2**32
