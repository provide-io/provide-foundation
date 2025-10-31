#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import sys

from provide.foundation.logger import get_logger
from provide.foundation.testmode.decorators import skip_in_test_mode

"""systemd integration utilities.

Provides utilities for notifying systemd about service status, implementing
watchdog functionality, and integrating with systemd's service management.

Automatically disabled in test mode (via @skip_in_test_mode decorator) to
prevent systemd notifications during testing, which would interfere with
test isolation and aren't meaningful in test contexts.

This module is Linux-specific and requires the optional 'sdnotify' package.
Install with: pip install provide-foundation[platform-linux]
"""

log = get_logger(__name__)

# Check if running on Linux
_IS_LINUX = sys.platform.startswith("linux")

# Try to import sdnotify (Linux only)
_HAS_SDNOTIFY = False
if _IS_LINUX:
    try:
        import sdnotify  # type: ignore[import-not-found]

        _HAS_SDNOTIFY = True
        _notifier = sdnotify.SystemdNotifier()
    except ImportError:
        _notifier = None
        log.debug(
            "sdnotify not available, systemd integration disabled",
            hint="Install with: pip install provide-foundation[platform-linux]",
        )
else:
    _notifier = None
    log.debug("systemd features only available on Linux", platform=sys.platform)


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_ready() -> bool:
    """Notify systemd that the service is ready.

    This should be called once the service has completed initialization and is
    ready to handle requests. For Type=notify services, systemd waits for this
    notification before considering the service started.

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Returns:
        True if notification sent successfully, False if sdnotify not available
        or running in test mode

    Example:
        >>> from provide.foundation.platform import notify_ready
        >>> # After service initialization
        >>> notify_ready()
        True

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug(
            "Cannot notify systemd - sdnotify not available",
            hint="Install with: pip install provide-foundation[platform-linux]",
        )
        return False

    try:
        _notifier.notify("READY=1")
        log.info("Notified systemd: service ready")
        return True
    except Exception as e:
        log.warning("Failed to notify systemd ready status", error=str(e))
        return False


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_status(status: str) -> bool:
    """Send status text to systemd.

    The status will be visible in systemctl status output.

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Args:
        status: Status message to send to systemd

    Returns:
        True if notification sent successfully, False if sdnotify not available

    Example:
        >>> from provide.foundation.platform import notify_status
        >>> notify_status("Processing requests: 42 active connections")
        True

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug(
            "Cannot notify systemd status - sdnotify not available",
            status=status,
        )
        return False

    try:
        _notifier.notify(f"STATUS={status}")
        log.debug("Notified systemd status", status=status)
        return True
    except Exception as e:
        log.warning("Failed to notify systemd status", status=status, error=str(e))
        return False


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_watchdog() -> bool:
    """Send watchdog keepalive to systemd.

    If WatchdogSec is configured in the systemd service unit, the service must
    call this periodically to prevent systemd from considering it hung and
    restarting it.

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Returns:
        True if notification sent successfully, False if sdnotify not available

    Example:
        >>> from provide.foundation.platform import notify_watchdog
        >>> import asyncio
        >>> async def watchdog_loop():
        ...     while True:
        ...         await asyncio.sleep(10)  # Must be < WatchdogSec
        ...         notify_watchdog()

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug("Cannot notify systemd watchdog - sdnotify not available")
        return False

    try:
        _notifier.notify("WATCHDOG=1")
        log.debug("Notified systemd watchdog")
        return True
    except Exception as e:
        log.warning("Failed to notify systemd watchdog", error=str(e))
        return False


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_reloading() -> bool:
    """Notify systemd that the service is reloading configuration.

    Call this at the beginning of configuration reload, and call notify_ready()
    when reload is complete.

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Returns:
        True if notification sent successfully, False if sdnotify not available

    Example:
        >>> from provide.foundation.platform import notify_reloading, notify_ready
        >>> notify_reloading()
        True
        >>> # Reload configuration
        >>> notify_ready()
        True

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug("Cannot notify systemd reload - sdnotify not available")
        return False

    try:
        _notifier.notify("RELOADING=1")
        log.info("Notified systemd: reloading")
        return True
    except Exception as e:
        log.warning("Failed to notify systemd reloading", error=str(e))
        return False


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_stopping() -> bool:
    """Notify systemd that the service is stopping.

    Call this at the beginning of graceful shutdown.

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Returns:
        True if notification sent successfully, False if sdnotify not available

    Example:
        >>> from provide.foundation.platform import notify_stopping
        >>> # At shutdown
        >>> notify_stopping()
        True
        >>> # Perform cleanup
        >>> # Exit

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug("Cannot notify systemd stopping - sdnotify not available")
        return False

    try:
        _notifier.notify("STOPPING=1")
        log.info("Notified systemd: stopping")
        return True
    except Exception as e:
        log.warning("Failed to notify systemd stopping", error=str(e))
        return False


@skip_in_test_mode(return_value=False, reason="systemd notifications not meaningful in tests")
def notify_error(errno: int, message: str | None = None) -> bool:
    """Notify systemd of an error condition.

    Args:
        errno: Error number (errno value)
        message: Optional error message

    Automatically disabled in test mode (via @skip_in_test_mode decorator).

    Returns:
        True if notification sent successfully, False if sdnotify not available

    Example:
        >>> from provide.foundation.platform import notify_error
        >>> import errno
        >>> notify_error(errno.ECONNREFUSED, "Failed to connect to database")
        True

    """
    if not _HAS_SDNOTIFY or _notifier is None:
        log.debug("Cannot notify systemd error - sdnotify not available")
        return False

    try:
        notification = f"ERRNO={errno}"
        _notifier.notify(notification)
        log.warning("Notified systemd error", errno=errno, message=message)
        return True
    except Exception as e:
        log.warning("Failed to notify systemd error", errno=errno, error=str(e))
        return False


def has_systemd() -> bool:
    """Check if systemd integration is available.

    Returns:
        True if running on Linux and sdnotify is installed, False otherwise

    Example:
        >>> from provide.foundation.platform import has_systemd
        >>> if has_systemd():
        ...     # Use systemd features
        ...     pass

    """
    return _HAS_SDNOTIFY


__all__ = [
    "has_systemd",
    "notify_error",
    "notify_ready",
    "notify_reloading",
    "notify_status",
    "notify_stopping",
    "notify_watchdog",
]

# 🧱🏗️🔚
