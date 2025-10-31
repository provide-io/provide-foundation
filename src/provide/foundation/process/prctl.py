#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import sys

from provide.foundation.errors.platform import PlatformError
from provide.foundation.logger import get_logger

"""Linux process control (prctl) utilities.

Provides access to Linux process control operations like capabilities,
death signals, and process restrictions.

This module is Linux-specific and requires the optional 'python-prctl' package.
Install with: pip install provide-foundation[process-linux]
"""

log = get_logger(__name__)

# Check if running on Linux
_IS_LINUX = sys.platform.startswith("linux")

# Try to import prctl (Linux only)
_HAS_PRCTL = False
if _IS_LINUX:
    try:
        import prctl  # type: ignore[import-not-found]

        _HAS_PRCTL = True
    except ImportError:
        log.debug(
            "python-prctl not available, Linux process control features disabled",
            hint="Install with: pip install provide-foundation[process-linux]",
        )
else:
    log.debug("prctl features only available on Linux", platform=sys.platform)


def _require_prctl() -> None:
    """Raise error if prctl is not available."""
    if not _IS_LINUX:
        raise PlatformError(
            f"prctl features are only available on Linux (current platform: {sys.platform})",
            code="PLATFORM_NOT_SUPPORTED",
            platform=sys.platform,
        )
    if not _HAS_PRCTL:
        raise PlatformError(
            "python-prctl is not installed",
            code="DEPENDENCY_MISSING",
            hint="Install with: pip install provide-foundation[process-linux]",
        )


def set_death_signal(signal: int) -> bool:
    """Set signal to be sent to process when parent dies (PR_SET_PDEATHSIG).

    This is useful for ensuring child processes are cleaned up when the parent
    terminates unexpectedly.

    Args:
        signal: Signal number to send (e.g., signal.SIGTERM, signal.SIGKILL)

    Returns:
        True if successful, False otherwise

    Raises:
        PlatformError: If not on Linux or python-prctl not installed

    Example:
        >>> import signal
        >>> from provide.foundation.process import set_death_signal
        >>> set_death_signal(signal.SIGTERM)  # Send SIGTERM when parent dies
        True

    """
    _require_prctl()

    try:
        prctl.set_pdeathsig(signal)
        log.debug("Death signal set", signal=signal)
        return True
    except Exception as e:
        log.warning("Failed to set death signal", signal=signal, error=str(e))
        return False


def set_dumpable(dumpable: bool) -> bool:
    """Set whether process can produce core dumps (PR_SET_DUMPABLE).

    Args:
        dumpable: True to allow core dumps, False to disable

    Returns:
        True if successful, False otherwise

    Raises:
        PlatformError: If not on Linux or python-prctl not installed

    Example:
        >>> from provide.foundation.process import set_dumpable
        >>> set_dumpable(False)  # Disable core dumps for security
        True

    """
    _require_prctl()

    try:
        prctl.set_dumpable(1 if dumpable else 0)
        log.debug("Dumpable flag set", dumpable=dumpable)
        return True
    except Exception as e:
        log.warning("Failed to set dumpable flag", dumpable=dumpable, error=str(e))
        return False


def set_name(name: str) -> bool:
    """Set process name (PR_SET_NAME).

    Note: This is different from setproctitle. PR_SET_NAME sets the comm value
    in /proc/[pid]/comm (limited to 16 bytes including null terminator).

    Args:
        name: Process name (max 15 characters)

    Returns:
        True if successful, False otherwise

    Raises:
        PlatformError: If not on Linux or python-prctl not installed

    Example:
        >>> from provide.foundation.process import set_name
        >>> set_name("worker-1")
        True

    """
    _require_prctl()

    if len(name) > 15:
        log.warning(
            "Process name truncated to 15 characters",
            requested=name,
            actual=name[:15],
        )
        name = name[:15]

    try:
        prctl.set_name(name)
        log.debug("Process name set", name=name)
        return True
    except Exception as e:
        log.warning("Failed to set process name", name=name, error=str(e))
        return False


def get_name() -> str | None:
    """Get process name (PR_GET_NAME).

    Returns:
        Process name, or None if prctl is not available

    Raises:
        PlatformError: If not on Linux or python-prctl not installed

    Example:
        >>> from provide.foundation.process import get_name
        >>> get_name()
        'worker-1'

    """
    _require_prctl()

    try:
        return prctl.get_name()
    except Exception as e:
        log.debug("Failed to get process name", error=str(e))
        return None


def set_no_new_privs(enabled: bool = True) -> bool:
    """Set no_new_privs flag (PR_SET_NO_NEW_PRIVS).

    When enabled, execve() will not grant privileges to do anything that could
    not have been done without the execve() call. This is a security feature.

    Args:
        enabled: True to enable no_new_privs, False to attempt disable (usually fails)

    Returns:
        True if successful, False otherwise

    Raises:
        PlatformError: If not on Linux or python-prctl not installed

    Example:
        >>> from provide.foundation.process import set_no_new_privs
        >>> set_no_new_privs(True)  # Prevent privilege escalation
        True

    """
    _require_prctl()

    try:
        # Note: python-prctl doesn't have direct no_new_privs support
        # This would require direct prctl() syscall
        import ctypes

        # PR_SET_NO_NEW_PRIVS = 38
        # PR_GET_NO_NEW_PRIVS = 39
        libc = ctypes.CDLL(None)
        result = libc.prctl(38, 1 if enabled else 0, 0, 0, 0)
        if result == 0:
            log.debug("no_new_privs flag set", enabled=enabled)
            return True
        log.warning("Failed to set no_new_privs flag", result=result)
        return False
    except Exception as e:
        log.warning("Failed to set no_new_privs flag", enabled=enabled, error=str(e))
        return False


def has_prctl() -> bool:
    """Check if prctl is available.

    Returns:
        True if running on Linux and python-prctl is installed, False otherwise

    Example:
        >>> from provide.foundation.process import has_prctl
        >>> if has_prctl():
        ...     # Use prctl features
        ...     pass

    """
    return _HAS_PRCTL


def is_linux() -> bool:
    """Check if running on Linux.

    Returns:
        True if running on Linux, False otherwise

    Example:
        >>> from provide.foundation.process import is_linux
        >>> is_linux()
        True

    """
    return _IS_LINUX


__all__ = [
    "get_name",
    "has_prctl",
    "is_linux",
    "set_death_signal",
    "set_dumpable",
    "set_name",
    "set_no_new_privs",
]

# 🧱🏗️🔚
