from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from pathlib import Path
from typing import Any

from provide.foundation.process.aio import async_run, async_shell, async_stream
from provide.foundation.process.runner import CompletedProcess

"""Async subprocess execution utilities.

This module provides backward-compatible wrappers for the refactored aio package.
New code should import directly from provide.foundation.process.aio.
"""


async def async_run_command(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    return await async_run(
        cmd=cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        input=input,
        shell=shell,
        **kwargs,
    )


async def async_stream_command(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    async for line in async_stream(
        cmd=cmd,
        cwd=cwd,
        env=env,
        timeout=timeout,
        stream_stderr=stream_stderr,
        **kwargs,
    ):
        yield line


async def async_run_shell(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command asynchronously.

    WARNING: This function uses shell=True, which can be dangerous with
    unsanitized input. Only use with trusted commands or properly sanitized input.

    Args:
        cmd: Shell command string (MUST be trusted/sanitized)
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout in seconds
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Security Note:
        This function enables shell interpretation of the command string,
        which allows shell features but also creates injection risks.
        Use async_run_command with a list for safer execution.
    """
    return await async_shell(
        cmd=cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        **kwargs,
    )


__all__ = [
    "async_run_command",
    "async_run_shell",
    "async_stream_command",
]
