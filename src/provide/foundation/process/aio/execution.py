# provide/foundation/process/aio/execution.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import builtins
from collections.abc import Mapping
import contextlib
from pathlib import Path
from typing import Any

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import (
    CompletedProcess,
    filter_subprocess_kwargs,
    prepare_environment,
)

"""Core async subprocess execution."""

log = get_logger(__name__)


async def create_subprocess(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def read_stream_continuously(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def communicate_with_timeout(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


def create_completed_process_result(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def check_process_success(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


async def cleanup_process(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def async_run(
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
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


# <3 🧱🤝🏃🪄
