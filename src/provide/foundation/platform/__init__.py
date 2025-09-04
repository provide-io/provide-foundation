"""Platform detection and system information utilities.

All platform-related functions in one place for easy discovery and use.
"""

from dataclasses import dataclass
import os
import platform
import re
import shutil

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

plog = get_logger(__name__)


class PlatformError(FoundationError):
    """Error in platform detection."""
    pass


@dataclass
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


# ============================================================================
# Core Detection Functions
# ============================================================================

def get_os() -> str:
    """
    Get normalized OS name.
    
    Returns:
        Normalized OS name (darwin, linux, windows)
    """
    try:
        os_name = platform.system().lower()
        if os_name in ("darwin", "macos"):
            return "darwin"
        return os_name
    except Exception as e:
        plog.error("Failed to detect OS", error=str(e))
        raise PlatformError(
            "Failed to detect operating system",
            code="PLATFORM_OS_DETECTION_FAILED",
            error=str(e)
        ) from e


def get_arch() -> str:
    """
    Get normalized architecture name.
    
    Returns:
        Normalized architecture (amd64, arm64, x86, i386)
    """
    try:
        arch = platform.machine().lower()
        # Normalize common architectures
        if arch in ["x86_64", "amd64"]:
            return "amd64"
        elif arch in ["aarch64", "arm64"]:
            return "arm64"
        elif arch in ["i686", "i586", "i486"]:
            return "x86"
        elif arch in ["i386"]:
            return "386"
        return arch
    except Exception as e:
        plog.error("Failed to detect architecture", error=str(e))
        raise PlatformError(
            "Failed to detect architecture",
            code="PLATFORM_ARCH_DETECTION_FAILED",
            error=str(e)
        ) from e


def get_platform() -> str:
    """
    Get normalized platform string in format 'os_arch'.
    
    Returns:
        Platform string like 'darwin_arm64' or 'linux_amd64'
    """
    os_name = get_os()
    arch = get_arch()
    platform_str = f"{os_name}_{arch}"
    plog.debug("Detected platform", platform=platform_str, os=os_name, arch=arch)
    return platform_str


def get_os_version() -> str | None:
    """
    Get OS version information.
    
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
        plog.warning("Failed to detect OS version", error=str(e))
    
    return None


def get_cpu_type() -> str | None:
    """
    Get CPU type/family information.
    
    Returns:
        CPU type string or None if unavailable
    """
    try:
        processor = platform.processor()
        if processor:
            # Clean up common processor strings
            if "Intel" in processor:
                # Extract Intel CPU model
                if "Core" in processor:
                    match = re.search(r"Core\(TM\)\s+(\w+)", processor)
                    if match:
                        return f"Intel Core {match.group(1)}"
                return "Intel"
            elif "AMD" in processor:
                # Extract AMD CPU model
                if "Ryzen" in processor:
                    match = re.search(r"Ryzen\s+(\d+)", processor)
                    if match:
                        return f"AMD Ryzen {match.group(1)}"
                return "AMD"
            elif "Apple" in processor or "M1" in processor or "M2" in processor or "M3" in processor:
                # Apple Silicon
                match = re.search(r"(M\d+\w*)", processor)
                if match:
                    return f"Apple {match.group(1)}"
                return "Apple Silicon"
            elif processor:
                # Return cleaned processor string
                return processor.strip()
    except Exception as e:
        plog.warning("Failed to detect CPU type", error=str(e))
    
    return None


def get_system_info() -> SystemInfo:
    """
    Gather comprehensive system information.
    
    Returns:
        SystemInfo object with all available system details
    """
    # Basic platform info
    os_name = get_os()
    arch = get_arch()
    platform_str = get_platform()
    os_version = get_os_version()
    cpu_type = get_cpu_type()
    
    # Python info
    python_version = platform.python_version()
    
    # System info
    hostname = None
    try:
        hostname = platform.node()
    except Exception:
        pass
    
    # User info
    username = os.environ.get("USER") or os.environ.get("USERNAME")
    home_dir = os.path.expanduser("~")
    temp_dir = os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp"
    
    # CPU info
    num_cpus = None
    try:
        num_cpus = os.cpu_count()
    except Exception:
        pass
    
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


# ============================================================================
# Helper Functions
# ============================================================================

def normalize_platform_components(os_name: str, arch_name: str) -> tuple[str, str]:
    """
    Normalize OS and architecture names to standard format.
    
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
        "i386": "386",
        "386": "386",
    }
    
    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())
    
    return normalized_os, normalized_arch


def normalize_arch(arch: str) -> str:
    """Normalize architecture name to standard format."""
    _, normalized = normalize_platform_components("linux", arch)
    return normalized


def normalize_os(os_name: str) -> str:
    """Normalize OS name to standard format."""
    normalized, _ = normalize_platform_components(os_name, "amd64")
    return normalized


# ============================================================================
# Boolean Helpers
# ============================================================================

def is_windows() -> bool:
    """Check if running on Windows."""
    return get_os() == "windows"


def is_macos() -> bool:
    """Check if running on macOS."""
    return get_os() == "darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return get_os() == "linux"


def is_arm() -> bool:
    """Check if running on ARM architecture."""
    arch = get_arch()
    return arch in ["arm64", "arm", "aarch64"]


def is_64bit() -> bool:
    """Check if running on 64-bit architecture."""
    arch = get_arch()
    return arch in ["amd64", "arm64", "x86_64", "aarch64"]


# ============================================================================
# Tool-Specific Functions
# ============================================================================

def get_executable_extension() -> str:
    """Get platform-specific executable extension."""
    return ".exe" if is_windows() else ""


def get_archive_extension() -> str:
    """Get platform-appropriate archive extension."""
    return ".zip" if is_windows() else ".tar.gz"


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "get_os",
    "get_arch",
    "get_platform",
    "get_os_version",
    "get_cpu_type",
    "get_system_info",
    "normalize_platform_components",
    "normalize_arch",
    "normalize_os",
    "is_windows",
    "is_macos",
    "is_linux",
    "is_arm",
    "is_64bit",
    "get_executable_extension",
    "get_archive_extension",
    "SystemInfo",
    "PlatformError",
]