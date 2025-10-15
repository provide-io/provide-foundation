# provide/foundation/logger/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
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
