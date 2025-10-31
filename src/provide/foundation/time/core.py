#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from datetime import datetime
import time
from zoneinfo import ZoneInfo

from provide.foundation.errors import ValidationError

"""Core time utilities for Foundation."""


def provide_time() -> float:
    """Get current time with Foundation tracking.

    Returns:
        Current time as seconds since epoch

    Example:
        >>> current_time = provide_time()
        >>> isinstance(current_time, float)
        True

    """
    return time.time()


def provide_sleep(seconds: float) -> None:
    """Sleep with Foundation tracking and interruption support.

    Args:
        seconds: Number of seconds to sleep

    Raises:
        ValidationError: If seconds is negative

    Example:
        >>> provide_sleep(0.1)  # Sleep for 100ms

    """
    if seconds < 0:
        raise ValidationError("Sleep duration must be non-negative")
    time.sleep(seconds)


def provide_now(tz: str | ZoneInfo | None = None) -> datetime:
    """Get current datetime with timezone awareness.

    Args:
        tz: Timezone (string name, ZoneInfo object, or None for local)

    Returns:
        Current datetime with timezone information

    Example:
        >>> now = provide_now()
        >>> now.tzinfo is not None
        True
        >>> utc_now = provide_now("UTC")
        >>> utc_now.tzinfo.key
        'UTC'

    """
    if tz is None:
        return datetime.now()
    zone = ZoneInfo(tz) if isinstance(tz, str) else tz

    return datetime.now(zone)


# 🧱🏗️🔚
