from __future__ import annotations

from provide.foundation.errors.runtime import ProcessError
from provide.foundation.process.async_runner import (
    async_run_command,
    async_run_shell,
    async_stream_command,
)
from provide.foundation.process.exit import (
    exit_error,
    exit_interrupted,
    exit_success,
)
from provide.foundation.process.lifecycle import (
    ManagedProcess,
    wait_for_process_output,
)
from provide.foundation.process.runner import (
    CompletedProcess,
    run_command,
    run_shell,
    stream_command,
)

"""Process execution utilities.

Provides sync and async subprocess execution with consistent error handling,
and advanced process lifecycle management.
"""

__all__ = [
    # Core types
    "CompletedProcess",
    # Process lifecycle management
    "ManagedProcess",
    "ProcessError",
    # Async execution
    "async_run_command",
    "async_run_shell",
    "async_stream_command",
    "exit_error",
    "exit_interrupted",
    # Exit utilities
    "exit_success",
    # Sync execution
    "run_command",
    "run_shell",
    "stream_command",
    "wait_for_process_output",
]
