#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# provide/foundation/errors/process.py
#
from typing import Any

from provide.foundation.errors.base import FoundationError

"""Process execution related errors."""


class ProcessError(FoundationError):
    """Error for external process execution failures with output capture."""

    def __init__(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def _default_code(self) -> str:
        """Return default error code for process errors."""
        return "PROCESS_ERROR"


class CommandNotFoundError(ProcessError):
    """Error when a command/executable is not found."""

    def _default_code(self) -> str:
        return "COMMAND_NOT_FOUND"


class ProcessTimeoutError(ProcessError):
    """Error when a process times out."""

    def __init__(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def _default_code(self) -> str:
        return "PROCESS_TIMEOUT"


# 🧱🏗️🔚
