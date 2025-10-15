# provide/foundation/process/aio/streaming.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import builtins
from collections.abc import AsyncIterator, Mapping
from pathlib import Path
from typing import Any

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import filter_subprocess_kwargs, prepare_environment

"""Async subprocess streaming execution."""

log = get_logger(__name__)


async def create_stream_subprocess(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def read_lines_with_timeout(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def cleanup_stream_process(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


def check_stream_exit_code(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


async def async_stream(
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
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


# <3 🧱🤝🏃🪄
