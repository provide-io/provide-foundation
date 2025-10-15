# provide/foundation/process/sync/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
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
