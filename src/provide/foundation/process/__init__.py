#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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
from provide.foundation.process.prctl import (
    get_name,
    has_prctl,
    is_linux,
    set_death_signal,
    set_dumpable,
    set_name,
    set_no_new_privs,
)
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.sync import run, run_simple, shell, stream
from provide.foundation.process.title import (
    get_process_title,
    has_setproctitle,
    set_process_title,
    set_process_title_from_argv,
)

"""Process Execution Subsystem.

Provides an opinionated system for sync and async subprocess execution,
integrated with the framework's security model (command validation,
environment scrubbing) and logging. It also includes components for
advanced process lifecycle management, process title management, and
Linux-specific process control features.
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
    # Linux process control (optional: python-prctl, Linux only)
    "get_name",
    # Process title management (optional: setproctitle)
    "get_process_title",
    "has_prctl",
    "has_setproctitle",
    "is_linux",
    # Sync execution
    "run",
    "run_simple",
    "set_death_signal",
    "set_dumpable",
    "set_name",
    "set_no_new_privs",
    "set_process_title",
    "set_process_title_from_argv",
    "shell",
    "stream",
    "wait_for_process_output",
]

# 🧱🏗️🔚
