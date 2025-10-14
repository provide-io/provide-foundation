# provide/foundation/process/aio/__init__.py
#
# This is the provide.io LLC 2025 Copyright. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.process.aio.execution import async_run
from provide.foundation.process.aio.shell import async_shell
from provide.foundation.process.aio.streaming import async_stream

"""Async subprocess execution utilities."""

__all__ = [
    "async_run",
    "async_shell",
    "async_stream",
]


# <3 🧱🤝🏃🪄
