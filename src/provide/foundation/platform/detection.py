"""Core platform detection functions."""

import platform
import re

from provide.foundation.errors.platform import PlatformError
from provide.foundation.logger import get_logger

plog = get_logger(__name__)


def get_os_name() -> str:
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
            error=str(e),
        ) from e


def get_arch_name() -> str:
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
        return arch
    except Exception as e:
        plog.error("Failed to detect architecture", error=str(e))
        raise PlatformError(
            "Failed to detect architecture",
            code="PLATFORM_ARCH_DETECTION_FAILED",
            error=str(e),
        ) from e


def get_platform_string() -> str:
    """
    Get normalized platform string in format 'os_arch'.

    Returns:
        Platform string like 'darwin_arm64' or 'linux_amd64'
    """
    os_name = get_os_name()
    arch = get_arch_name()
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
            elif (
                "Apple" in processor
                or "M1" in processor
                or "M2" in processor
                or "M3" in processor
            ):
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
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch
