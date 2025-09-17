from __future__ import annotations

import asyncio
import builtins
from collections.abc import AsyncIterator, Mapping
import os
from pathlib import Path
from typing import Any

from provide.foundation.logger import get_logger
from provide.foundation.process.runner import (
    CompletedProcess,
    ProcessError,
    TimeoutError,
)

"""Async subprocess execution utilities."""

plog = get_logger(__name__)


def _filter_subprocess_kwargs(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters."""
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
        "executable",
        "preexec_fn",
        "close_fds",
        "group",
        "extra_groups",
        "user",
        "umask",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def _prepare_async_environment(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for async process execution."""
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")
    return run_env


async def _create_subprocess(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess."""
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **_filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def _communicate_with_timeout(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout."""
    if timeout:
        try:
            return await asyncio.wait_for(
                process.communicate(input=input),
                timeout=timeout,
            )
        except builtins.TimeoutError as e:
            process.kill()
            await process.wait()
            plog.error("⏱️ Async command timed out", command=cmd_str, timeout=timeout)
            raise TimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout=timeout,
            ) from e
    else:
        return await process.communicate(input=input)


def _create_completed_process(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results."""
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd,
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(run_env) if env else None,
    )


def _check_process_success(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed."""
    if check and process.returncode != 0:
        plog.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            returncode=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


async def _cleanup_process(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources."""
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
        **kwargs: Additional arguments

    Returns:
        CompletedProcess with results

    Raises:
        ProcessError: If command fails and check=True
        TimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🚀 Running async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and convert Path to string
    run_env = _prepare_async_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await _create_subprocess(
            cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs
        )

        try:
            # Communicate with process
            stdout, stderr = await _communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = _create_completed_process(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            _check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            plog.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise

        plog.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
            error=str(e),
        ) from e


def _prepare_stream_environment(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare the environment for process execution."""
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")
    return run_env


async def _create_stream_subprocess(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming."""
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **_filter_subprocess_kwargs(kwargs),
    )


async def _read_lines_with_timeout(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout."""
    lines = []
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
        plog.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise TimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout=timeout,
        ) from e

    return lines


async def _cleanup_stream_process(process: Any) -> None:
    """Clean up subprocess resources."""
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


def _check_process_exit_code(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully."""
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            returncode=process.returncode,
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
        **kwargs: Additional arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        TimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = _prepare_stream_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await _create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await _read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                _check_process_exit_code(process, cmd_str)

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
                _check_process_exit_code(process, cmd_str)

            plog.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await _cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise

        plog.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e


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
        timeout: Command timeout
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Security Note:
        This function enables shell interpretation of the command string,
        which allows shell features but also creates injection risks.
        Use async_run_command with a list for safer execution.

    """
    return await async_run_command(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with caller validation
        **kwargs,
    )
