# provide/foundation/logger/processors/__init__.py
#
# This is the provide.io LLC 2025 Copyright. All rights reserved.
#
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
