# provide/foundation/time/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.time.core import (
    provide_now,
    provide_sleep,
    provide_time,
)

"""Production time utilities for Foundation.

Provides consistent time handling with Foundation integration,
better testability, and timezone awareness.
"""

__all__ = [
    "provide_now",
    "provide_sleep",
    "provide_time",
]


# <3 🧱🤝🕰️🪄
