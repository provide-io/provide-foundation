#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from attrs import define

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.process import ProcessError

"""Shared utilities for both sync and async subprocess execution."""


@define(slots=True)
class CompletedProcess:
    """Result of a completed process.

    Note:
        The `env` field only stores caller-provided environment variable overrides,
        not the full subprocess environment. This prevents credential leakage when
        CompletedProcess objects are logged or stored.
    """

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    cwd: str | None = None
    env: dict[str, str] | None = None  # Only caller overrides, not full environment


def prepare_environment(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(caller_overrides=env, scrub=True)


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


def normalize_cwd(cwd: str | Path | None) -> str | None:
    """Normalize working directory to string.

    Args:
        cwd: Working directory as string, Path, or None

    Returns:
        Working directory as string or None
    """
    if isinstance(cwd, Path):
        return str(cwd)
    return cwd


def prepare_input(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def validate_command_type(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


# 🧱🏗️🔚
