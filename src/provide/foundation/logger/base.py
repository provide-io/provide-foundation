# provide/foundation/logger/base.py
#
# This is the provide.io LLC 2025 Copyright. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# base.py
#
from provide.foundation.logger.core import FoundationLogger, logger
from provide.foundation.logger.factories import get_logger

"""Foundation Logger - Main Interface.

Re-exports the core logger components.
"""

__all__ = [
    "FoundationLogger",
    "get_logger",
    "logger",
]


# <3 🧱🤝📝🪄
