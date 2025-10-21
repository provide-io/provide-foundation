# provide/foundation/platform/detection.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import platform
import re

from provide.foundation.errors.platform import PlatformError
from provide.foundation.logger import get_logger
from provide.foundation.utils.caching import cached

"""Core platform detection functions."""

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


def x__detect_intel_cpu__mutmut_orig(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_1(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "XXIntelXX" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_2(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_3(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "INTEL" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_4(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_5(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "XXCoreXX" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_6(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_7(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "CORE" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_8(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" not in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_9(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = None
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_10(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(None, processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_11(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", None)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_12(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_13(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", )
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_14(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"XXCore\(TM\)\s+(\w+)XX", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_15(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"core\(tm\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_16(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"CORE\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_17(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(None)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_18(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(2)}"
    return "Intel"


def x__detect_intel_cpu__mutmut_19(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "XXIntelXX"


def x__detect_intel_cpu__mutmut_20(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "intel"


def x__detect_intel_cpu__mutmut_21(processor: str) -> str | None:
    """Detect Intel CPU type from processor string."""
    if "Intel" not in processor:
        return None

    if "Core" in processor:
        match = re.search(r"Core\(TM\)\s+(\w+)", processor)
        if match:
            return f"Intel Core {match.group(1)}"
    return "INTEL"

x__detect_intel_cpu__mutmut_mutants : ClassVar[MutantDict] = {
'x__detect_intel_cpu__mutmut_1': x__detect_intel_cpu__mutmut_1, 
    'x__detect_intel_cpu__mutmut_2': x__detect_intel_cpu__mutmut_2, 
    'x__detect_intel_cpu__mutmut_3': x__detect_intel_cpu__mutmut_3, 
    'x__detect_intel_cpu__mutmut_4': x__detect_intel_cpu__mutmut_4, 
    'x__detect_intel_cpu__mutmut_5': x__detect_intel_cpu__mutmut_5, 
    'x__detect_intel_cpu__mutmut_6': x__detect_intel_cpu__mutmut_6, 
    'x__detect_intel_cpu__mutmut_7': x__detect_intel_cpu__mutmut_7, 
    'x__detect_intel_cpu__mutmut_8': x__detect_intel_cpu__mutmut_8, 
    'x__detect_intel_cpu__mutmut_9': x__detect_intel_cpu__mutmut_9, 
    'x__detect_intel_cpu__mutmut_10': x__detect_intel_cpu__mutmut_10, 
    'x__detect_intel_cpu__mutmut_11': x__detect_intel_cpu__mutmut_11, 
    'x__detect_intel_cpu__mutmut_12': x__detect_intel_cpu__mutmut_12, 
    'x__detect_intel_cpu__mutmut_13': x__detect_intel_cpu__mutmut_13, 
    'x__detect_intel_cpu__mutmut_14': x__detect_intel_cpu__mutmut_14, 
    'x__detect_intel_cpu__mutmut_15': x__detect_intel_cpu__mutmut_15, 
    'x__detect_intel_cpu__mutmut_16': x__detect_intel_cpu__mutmut_16, 
    'x__detect_intel_cpu__mutmut_17': x__detect_intel_cpu__mutmut_17, 
    'x__detect_intel_cpu__mutmut_18': x__detect_intel_cpu__mutmut_18, 
    'x__detect_intel_cpu__mutmut_19': x__detect_intel_cpu__mutmut_19, 
    'x__detect_intel_cpu__mutmut_20': x__detect_intel_cpu__mutmut_20, 
    'x__detect_intel_cpu__mutmut_21': x__detect_intel_cpu__mutmut_21
}

def _detect_intel_cpu(*args, **kwargs):
    result = _mutmut_trampoline(x__detect_intel_cpu__mutmut_orig, x__detect_intel_cpu__mutmut_mutants, args, kwargs)
    return result 

_detect_intel_cpu.__signature__ = _mutmut_signature(x__detect_intel_cpu__mutmut_orig)
x__detect_intel_cpu__mutmut_orig.__name__ = 'x__detect_intel_cpu'


def x__detect_amd_cpu__mutmut_orig(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_1(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "XXAMDXX" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_2(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "amd" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_3(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_4(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "XXRyzenXX" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_5(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_6(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "RYZEN" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_7(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" not in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_8(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = None
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_9(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(None, processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_10(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", None)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_11(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_12(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", )
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_13(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"XXRyzen\s+(\d+)XX", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_14(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_15(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"RYZEN\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_16(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(None)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_17(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(2)}"
    return "AMD"


def x__detect_amd_cpu__mutmut_18(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "XXAMDXX"


def x__detect_amd_cpu__mutmut_19(processor: str) -> str | None:
    """Detect AMD CPU type from processor string."""
    if "AMD" not in processor:
        return None

    if "Ryzen" in processor:
        match = re.search(r"Ryzen\s+(\d+)", processor)
        if match:
            return f"AMD Ryzen {match.group(1)}"
    return "amd"

x__detect_amd_cpu__mutmut_mutants : ClassVar[MutantDict] = {
'x__detect_amd_cpu__mutmut_1': x__detect_amd_cpu__mutmut_1, 
    'x__detect_amd_cpu__mutmut_2': x__detect_amd_cpu__mutmut_2, 
    'x__detect_amd_cpu__mutmut_3': x__detect_amd_cpu__mutmut_3, 
    'x__detect_amd_cpu__mutmut_4': x__detect_amd_cpu__mutmut_4, 
    'x__detect_amd_cpu__mutmut_5': x__detect_amd_cpu__mutmut_5, 
    'x__detect_amd_cpu__mutmut_6': x__detect_amd_cpu__mutmut_6, 
    'x__detect_amd_cpu__mutmut_7': x__detect_amd_cpu__mutmut_7, 
    'x__detect_amd_cpu__mutmut_8': x__detect_amd_cpu__mutmut_8, 
    'x__detect_amd_cpu__mutmut_9': x__detect_amd_cpu__mutmut_9, 
    'x__detect_amd_cpu__mutmut_10': x__detect_amd_cpu__mutmut_10, 
    'x__detect_amd_cpu__mutmut_11': x__detect_amd_cpu__mutmut_11, 
    'x__detect_amd_cpu__mutmut_12': x__detect_amd_cpu__mutmut_12, 
    'x__detect_amd_cpu__mutmut_13': x__detect_amd_cpu__mutmut_13, 
    'x__detect_amd_cpu__mutmut_14': x__detect_amd_cpu__mutmut_14, 
    'x__detect_amd_cpu__mutmut_15': x__detect_amd_cpu__mutmut_15, 
    'x__detect_amd_cpu__mutmut_16': x__detect_amd_cpu__mutmut_16, 
    'x__detect_amd_cpu__mutmut_17': x__detect_amd_cpu__mutmut_17, 
    'x__detect_amd_cpu__mutmut_18': x__detect_amd_cpu__mutmut_18, 
    'x__detect_amd_cpu__mutmut_19': x__detect_amd_cpu__mutmut_19
}

def _detect_amd_cpu(*args, **kwargs):
    result = _mutmut_trampoline(x__detect_amd_cpu__mutmut_orig, x__detect_amd_cpu__mutmut_mutants, args, kwargs)
    return result 

_detect_amd_cpu.__signature__ = _mutmut_signature(x__detect_amd_cpu__mutmut_orig)
x__detect_amd_cpu__mutmut_orig.__name__ = 'x__detect_amd_cpu'


def x__detect_apple_cpu__mutmut_orig(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_1(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_2(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(None):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_3(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword not in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_4(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["XXAppleXX", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_5(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_6(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["APPLE", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_7(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "XXM1XX", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_8(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "m1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_9(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "XXM2XX", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_10(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "m2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_11(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "XXM3XX"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_12(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "m3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_13(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = None
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_14(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(None, processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_15(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", None)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_16(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_17(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", )
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_18(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"XX(M\d+\w*)XX", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_19(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(m\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_20(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_21(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(None)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_22(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(2)}"
    return "Apple Silicon"


def x__detect_apple_cpu__mutmut_23(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "XXApple SiliconXX"


def x__detect_apple_cpu__mutmut_24(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "apple silicon"


def x__detect_apple_cpu__mutmut_25(processor: str) -> str | None:
    """Detect Apple CPU type from processor string."""
    if not any(keyword in processor for keyword in ["Apple", "M1", "M2", "M3"]):
        return None

    match = re.search(r"(M\d+\w*)", processor)
    if match:
        return f"Apple {match.group(1)}"
    return "APPLE SILICON"

x__detect_apple_cpu__mutmut_mutants : ClassVar[MutantDict] = {
'x__detect_apple_cpu__mutmut_1': x__detect_apple_cpu__mutmut_1, 
    'x__detect_apple_cpu__mutmut_2': x__detect_apple_cpu__mutmut_2, 
    'x__detect_apple_cpu__mutmut_3': x__detect_apple_cpu__mutmut_3, 
    'x__detect_apple_cpu__mutmut_4': x__detect_apple_cpu__mutmut_4, 
    'x__detect_apple_cpu__mutmut_5': x__detect_apple_cpu__mutmut_5, 
    'x__detect_apple_cpu__mutmut_6': x__detect_apple_cpu__mutmut_6, 
    'x__detect_apple_cpu__mutmut_7': x__detect_apple_cpu__mutmut_7, 
    'x__detect_apple_cpu__mutmut_8': x__detect_apple_cpu__mutmut_8, 
    'x__detect_apple_cpu__mutmut_9': x__detect_apple_cpu__mutmut_9, 
    'x__detect_apple_cpu__mutmut_10': x__detect_apple_cpu__mutmut_10, 
    'x__detect_apple_cpu__mutmut_11': x__detect_apple_cpu__mutmut_11, 
    'x__detect_apple_cpu__mutmut_12': x__detect_apple_cpu__mutmut_12, 
    'x__detect_apple_cpu__mutmut_13': x__detect_apple_cpu__mutmut_13, 
    'x__detect_apple_cpu__mutmut_14': x__detect_apple_cpu__mutmut_14, 
    'x__detect_apple_cpu__mutmut_15': x__detect_apple_cpu__mutmut_15, 
    'x__detect_apple_cpu__mutmut_16': x__detect_apple_cpu__mutmut_16, 
    'x__detect_apple_cpu__mutmut_17': x__detect_apple_cpu__mutmut_17, 
    'x__detect_apple_cpu__mutmut_18': x__detect_apple_cpu__mutmut_18, 
    'x__detect_apple_cpu__mutmut_19': x__detect_apple_cpu__mutmut_19, 
    'x__detect_apple_cpu__mutmut_20': x__detect_apple_cpu__mutmut_20, 
    'x__detect_apple_cpu__mutmut_21': x__detect_apple_cpu__mutmut_21, 
    'x__detect_apple_cpu__mutmut_22': x__detect_apple_cpu__mutmut_22, 
    'x__detect_apple_cpu__mutmut_23': x__detect_apple_cpu__mutmut_23, 
    'x__detect_apple_cpu__mutmut_24': x__detect_apple_cpu__mutmut_24, 
    'x__detect_apple_cpu__mutmut_25': x__detect_apple_cpu__mutmut_25
}

def _detect_apple_cpu(*args, **kwargs):
    result = _mutmut_trampoline(x__detect_apple_cpu__mutmut_orig, x__detect_apple_cpu__mutmut_mutants, args, kwargs)
    return result 

_detect_apple_cpu.__signature__ = _mutmut_signature(x__detect_apple_cpu__mutmut_orig)
x__detect_apple_cpu__mutmut_orig.__name__ = 'x__detect_apple_cpu'


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


def x_normalize_platform_components__mutmut_orig(os_name: str, arch_name: str) -> tuple[str, str]:
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


def x_normalize_platform_components__mutmut_1(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = None

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


def x_normalize_platform_components__mutmut_2(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = {
        "XXlinuxXX": "linux",
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


def x_normalize_platform_components__mutmut_3(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = {
        "LINUX": "linux",
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


def x_normalize_platform_components__mutmut_4(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = {
        "linux": "XXlinuxXX",
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


def x_normalize_platform_components__mutmut_5(os_name: str, arch_name: str) -> tuple[str, str]:
    """Normalize OS and architecture names to standard format.

    Args:
        os_name: Operating system name
        arch_name: Architecture name

    Returns:
        Tuple of (normalized_os, normalized_arch)

    """
    # Normalize OS names
    os_map = {
        "linux": "LINUX",
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


def x_normalize_platform_components__mutmut_6(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXdarwinXX": "darwin",
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


def x_normalize_platform_components__mutmut_7(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "DARWIN": "darwin",
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


def x_normalize_platform_components__mutmut_8(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "darwin": "XXdarwinXX",
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


def x_normalize_platform_components__mutmut_9(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "darwin": "DARWIN",
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


def x_normalize_platform_components__mutmut_10(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXmacosXX": "darwin",
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


def x_normalize_platform_components__mutmut_11(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "MACOS": "darwin",
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


def x_normalize_platform_components__mutmut_12(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "macos": "XXdarwinXX",
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


def x_normalize_platform_components__mutmut_13(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "macos": "DARWIN",
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


def x_normalize_platform_components__mutmut_14(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXwindowsXX": "windows",
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


def x_normalize_platform_components__mutmut_15(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "WINDOWS": "windows",
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


def x_normalize_platform_components__mutmut_16(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "windows": "XXwindowsXX",
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


def x_normalize_platform_components__mutmut_17(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "windows": "WINDOWS",
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


def x_normalize_platform_components__mutmut_18(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXwin32XX": "windows",
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


def x_normalize_platform_components__mutmut_19(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "WIN32": "windows",
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


def x_normalize_platform_components__mutmut_20(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "win32": "XXwindowsXX",
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


def x_normalize_platform_components__mutmut_21(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "win32": "WINDOWS",
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


def x_normalize_platform_components__mutmut_22(os_name: str, arch_name: str) -> tuple[str, str]:
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
    arch_map = None

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_23(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXx86_64XX": "amd64",
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


def x_normalize_platform_components__mutmut_24(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "X86_64": "amd64",
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


def x_normalize_platform_components__mutmut_25(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "x86_64": "XXamd64XX",
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


def x_normalize_platform_components__mutmut_26(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "x86_64": "AMD64",
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


def x_normalize_platform_components__mutmut_27(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXamd64XX": "amd64",
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


def x_normalize_platform_components__mutmut_28(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "AMD64": "amd64",
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


def x_normalize_platform_components__mutmut_29(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "amd64": "XXamd64XX",
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


def x_normalize_platform_components__mutmut_30(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "amd64": "AMD64",
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


def x_normalize_platform_components__mutmut_31(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXaarch64XX": "arm64",
        "arm64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_32(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "AARCH64": "arm64",
        "arm64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_33(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "aarch64": "XXarm64XX",
        "arm64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_34(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "aarch64": "ARM64",
        "arm64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_35(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXarm64XX": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_36(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "ARM64": "arm64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_37(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "arm64": "XXarm64XX",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_38(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "arm64": "ARM64",
        "i686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_39(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXi686XX": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_40(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "I686": "x86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_41(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i686": "XXx86XX",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_42(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i686": "X86",
        "i586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_43(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXi586XX": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_44(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "I586": "x86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_45(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i586": "XXx86XX",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_46(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i586": "X86",
        "i486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_47(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXi486XX": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_48(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "I486": "x86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_49(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i486": "XXx86XX",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_50(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i486": "X86",
        "i386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_51(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "XXi386XX": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_52(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "I386": "i386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_53(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i386": "XXi386XX",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_54(os_name: str, arch_name: str) -> tuple[str, str]:
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
        "i386": "I386",
    }

    normalized_os = os_map.get(os_name.lower(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_55(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = None
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_56(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(None, os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_57(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(os_name.lower(), None)
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_58(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_59(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(os_name.lower(), )
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_60(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(os_name.upper(), os_name.lower())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_61(os_name: str, arch_name: str) -> tuple[str, str]:
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

    normalized_os = os_map.get(os_name.lower(), os_name.upper())
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_62(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = None

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_63(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(None, arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_64(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(arch_name.lower(), None)

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_65(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_66(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(arch_name.lower(), )

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_67(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(arch_name.upper(), arch_name.lower())

    return normalized_os, normalized_arch


def x_normalize_platform_components__mutmut_68(os_name: str, arch_name: str) -> tuple[str, str]:
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
    normalized_arch = arch_map.get(arch_name.lower(), arch_name.upper())

    return normalized_os, normalized_arch

x_normalize_platform_components__mutmut_mutants : ClassVar[MutantDict] = {
'x_normalize_platform_components__mutmut_1': x_normalize_platform_components__mutmut_1, 
    'x_normalize_platform_components__mutmut_2': x_normalize_platform_components__mutmut_2, 
    'x_normalize_platform_components__mutmut_3': x_normalize_platform_components__mutmut_3, 
    'x_normalize_platform_components__mutmut_4': x_normalize_platform_components__mutmut_4, 
    'x_normalize_platform_components__mutmut_5': x_normalize_platform_components__mutmut_5, 
    'x_normalize_platform_components__mutmut_6': x_normalize_platform_components__mutmut_6, 
    'x_normalize_platform_components__mutmut_7': x_normalize_platform_components__mutmut_7, 
    'x_normalize_platform_components__mutmut_8': x_normalize_platform_components__mutmut_8, 
    'x_normalize_platform_components__mutmut_9': x_normalize_platform_components__mutmut_9, 
    'x_normalize_platform_components__mutmut_10': x_normalize_platform_components__mutmut_10, 
    'x_normalize_platform_components__mutmut_11': x_normalize_platform_components__mutmut_11, 
    'x_normalize_platform_components__mutmut_12': x_normalize_platform_components__mutmut_12, 
    'x_normalize_platform_components__mutmut_13': x_normalize_platform_components__mutmut_13, 
    'x_normalize_platform_components__mutmut_14': x_normalize_platform_components__mutmut_14, 
    'x_normalize_platform_components__mutmut_15': x_normalize_platform_components__mutmut_15, 
    'x_normalize_platform_components__mutmut_16': x_normalize_platform_components__mutmut_16, 
    'x_normalize_platform_components__mutmut_17': x_normalize_platform_components__mutmut_17, 
    'x_normalize_platform_components__mutmut_18': x_normalize_platform_components__mutmut_18, 
    'x_normalize_platform_components__mutmut_19': x_normalize_platform_components__mutmut_19, 
    'x_normalize_platform_components__mutmut_20': x_normalize_platform_components__mutmut_20, 
    'x_normalize_platform_components__mutmut_21': x_normalize_platform_components__mutmut_21, 
    'x_normalize_platform_components__mutmut_22': x_normalize_platform_components__mutmut_22, 
    'x_normalize_platform_components__mutmut_23': x_normalize_platform_components__mutmut_23, 
    'x_normalize_platform_components__mutmut_24': x_normalize_platform_components__mutmut_24, 
    'x_normalize_platform_components__mutmut_25': x_normalize_platform_components__mutmut_25, 
    'x_normalize_platform_components__mutmut_26': x_normalize_platform_components__mutmut_26, 
    'x_normalize_platform_components__mutmut_27': x_normalize_platform_components__mutmut_27, 
    'x_normalize_platform_components__mutmut_28': x_normalize_platform_components__mutmut_28, 
    'x_normalize_platform_components__mutmut_29': x_normalize_platform_components__mutmut_29, 
    'x_normalize_platform_components__mutmut_30': x_normalize_platform_components__mutmut_30, 
    'x_normalize_platform_components__mutmut_31': x_normalize_platform_components__mutmut_31, 
    'x_normalize_platform_components__mutmut_32': x_normalize_platform_components__mutmut_32, 
    'x_normalize_platform_components__mutmut_33': x_normalize_platform_components__mutmut_33, 
    'x_normalize_platform_components__mutmut_34': x_normalize_platform_components__mutmut_34, 
    'x_normalize_platform_components__mutmut_35': x_normalize_platform_components__mutmut_35, 
    'x_normalize_platform_components__mutmut_36': x_normalize_platform_components__mutmut_36, 
    'x_normalize_platform_components__mutmut_37': x_normalize_platform_components__mutmut_37, 
    'x_normalize_platform_components__mutmut_38': x_normalize_platform_components__mutmut_38, 
    'x_normalize_platform_components__mutmut_39': x_normalize_platform_components__mutmut_39, 
    'x_normalize_platform_components__mutmut_40': x_normalize_platform_components__mutmut_40, 
    'x_normalize_platform_components__mutmut_41': x_normalize_platform_components__mutmut_41, 
    'x_normalize_platform_components__mutmut_42': x_normalize_platform_components__mutmut_42, 
    'x_normalize_platform_components__mutmut_43': x_normalize_platform_components__mutmut_43, 
    'x_normalize_platform_components__mutmut_44': x_normalize_platform_components__mutmut_44, 
    'x_normalize_platform_components__mutmut_45': x_normalize_platform_components__mutmut_45, 
    'x_normalize_platform_components__mutmut_46': x_normalize_platform_components__mutmut_46, 
    'x_normalize_platform_components__mutmut_47': x_normalize_platform_components__mutmut_47, 
    'x_normalize_platform_components__mutmut_48': x_normalize_platform_components__mutmut_48, 
    'x_normalize_platform_components__mutmut_49': x_normalize_platform_components__mutmut_49, 
    'x_normalize_platform_components__mutmut_50': x_normalize_platform_components__mutmut_50, 
    'x_normalize_platform_components__mutmut_51': x_normalize_platform_components__mutmut_51, 
    'x_normalize_platform_components__mutmut_52': x_normalize_platform_components__mutmut_52, 
    'x_normalize_platform_components__mutmut_53': x_normalize_platform_components__mutmut_53, 
    'x_normalize_platform_components__mutmut_54': x_normalize_platform_components__mutmut_54, 
    'x_normalize_platform_components__mutmut_55': x_normalize_platform_components__mutmut_55, 
    'x_normalize_platform_components__mutmut_56': x_normalize_platform_components__mutmut_56, 
    'x_normalize_platform_components__mutmut_57': x_normalize_platform_components__mutmut_57, 
    'x_normalize_platform_components__mutmut_58': x_normalize_platform_components__mutmut_58, 
    'x_normalize_platform_components__mutmut_59': x_normalize_platform_components__mutmut_59, 
    'x_normalize_platform_components__mutmut_60': x_normalize_platform_components__mutmut_60, 
    'x_normalize_platform_components__mutmut_61': x_normalize_platform_components__mutmut_61, 
    'x_normalize_platform_components__mutmut_62': x_normalize_platform_components__mutmut_62, 
    'x_normalize_platform_components__mutmut_63': x_normalize_platform_components__mutmut_63, 
    'x_normalize_platform_components__mutmut_64': x_normalize_platform_components__mutmut_64, 
    'x_normalize_platform_components__mutmut_65': x_normalize_platform_components__mutmut_65, 
    'x_normalize_platform_components__mutmut_66': x_normalize_platform_components__mutmut_66, 
    'x_normalize_platform_components__mutmut_67': x_normalize_platform_components__mutmut_67, 
    'x_normalize_platform_components__mutmut_68': x_normalize_platform_components__mutmut_68
}

def normalize_platform_components(*args, **kwargs):
    result = _mutmut_trampoline(x_normalize_platform_components__mutmut_orig, x_normalize_platform_components__mutmut_mutants, args, kwargs)
    return result 

normalize_platform_components.__signature__ = _mutmut_signature(x_normalize_platform_components__mutmut_orig)
x_normalize_platform_components__mutmut_orig.__name__ = 'x_normalize_platform_components'


# <3 🧱🤝🏗️🪄
