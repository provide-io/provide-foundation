# provide/foundation/process/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.errors.process import ProcessError
from provide.foundation.process.aio import async_run, async_shell, async_stream
from provide.foundation.process.exit import (
    exit_error,
    exit_interrupted,
    exit_success,
)
from provide.foundation.process.lifecycle import (
    ManagedProcess,
    wait_for_process_output,
)
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.sync import run, run_simple, shell, stream

"""Process Execution Subsystem.

Provides an opinionated system for sync and async subprocess execution,
integrated with the framework's security model (command validation,
environment scrubbing) and logging. It also includes components for
advanced process lifecycle management.
"""

__all__ = [
    # Core types
    "CompletedProcess",
    # Process lifecycle management
    "ManagedProcess",
    "ProcessError",
    # Async execution (modern API)
    "async_run",
    "async_shell",
    "async_stream",
    # Exit utilities
    "exit_error",
    "exit_interrupted",
    "exit_success",
    # Sync execution
    "run",
    "run_simple",
    "shell",
    "stream",
    "wait_for_process_output",
]


# <3 🧱🤝🏃🪄
