"""Process execution utilities.

Provides sync and async subprocess execution with consistent error handling,
and advanced process lifecycle management.
"""

from provide.foundation.errors.runtime import ProcessError
from provide.foundation.process.async_runner import (
    async_run_command,
    async_run_shell,
    async_stream_command,
)
from provide.foundation.process.exit import (
    exit_success,
    exit_error,
    exit_interrupted,
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

__all__ = [
    # Core types
    "CompletedProcess",
    "ProcessError",
    # Sync execution
    "run_command",
    "run_shell",
    "stream_command",
    # Async execution
    "async_run_command",
    "async_run_shell",
    "async_stream_command",
    # Process lifecycle management
    "ManagedProcess",
    "wait_for_process_output",
    # Exit utilities
    "exit_success",
    "exit_error",
    "exit_interrupted",
]
