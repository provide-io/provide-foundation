# provide/foundation/logger/processors/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.logger.processors.main import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)
from provide.foundation.logger.processors.trace import inject_trace_context

"""Processors package for Foundation logging."""

__all__ = [
    "_build_core_processors_list",
    "_build_formatter_processors_list",
    "inject_trace_context",
]


# <3 🧱🤝📝🪄
