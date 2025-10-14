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

"""Process execution utilities.

Provides sync and async subprocess execution with consistent error handling,
and advanced process lifecycle management.
"""

# Backward compatibility aliases (used by wrknv and flavorpack)
run_command = run
stream_command = stream

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
    # Sync execution (modern API)
    "run",
    # Backward compatibility (used by other projects)
    "run_command",
    "run_simple",
    "shell",
    "stream",
    "stream_command",
    "wait_for_process_output",
]
