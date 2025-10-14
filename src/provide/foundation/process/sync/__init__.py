# provide/foundation/process/sync/__init__.py
#
# This is the provide.io LLC 2025 Copyright. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.process.sync.execution import run, run_simple
from provide.foundation.process.sync.shell import shell
from provide.foundation.process.sync.streaming import stream

"""Sync subprocess execution utilities."""

__all__ = [
    "run",
    "run_simple",
    "shell",
    "stream",
]


# <3 🧱🤝🏃🪄
