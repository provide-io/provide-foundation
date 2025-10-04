from __future__ import annotations

from collections.abc import Mapping
import os
from typing import Any

from provide.foundation.errors.process import ProcessError
from provide.foundation.process.runner import CompletedProcess

"""Shared utilities for both sync and async subprocess execution."""


def prepare_environment(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution.

    Args:
        env: Optional environment variables to merge with current environment

    Returns:
        Dictionary of environment variables with telemetry disabled
    """
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    # Disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")
    return run_env


def create_completed_process(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def check_process_success(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def check_process_exit_code(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def filter_subprocess_kwargs(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}
