#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from pathlib import Path
import subprocess
import sys
from typing import Any

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import normalize_cwd, prepare_environment

"""Sync subprocess streaming execution."""

log = get_logger(__name__)


def _make_stdout_nonblocking(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling.

    Note:
        This is a no-op on Windows as fcntl module doesn't exist.
        Windows uses different mechanisms for non-blocking I/O.
    """
    if sys.platform == "win32":
        # Windows doesn't support fcntl; non-blocking I/O uses different APIs
        # For basic streaming, we can skip this on Windows
        return

    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def _check_timeout_expired(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def _read_chunk_from_stdout(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def _yield_complete_lines(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.rstrip(), buffer


def _yield_remaining_lines(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split("\n"):
        if line:
            yield line.rstrip()


def _finalize_remaining_data(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer += remaining_data

    yield from _yield_remaining_lines(buffer)


def _stream_with_timeout(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling.

    Note:
        On Windows, uses polling instead of select since select.select
        only works with sockets on Windows, not file descriptors.
    """
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Check if data is available
        # On Unix: Use select
        # On Windows: Use simple polling (select doesn't work with pipes)
        if sys.platform == "win32":
            # Windows: Simple polling with small sleep
            import time

            elapsed = time.time() - start_time
            remaining = timeout - elapsed

            # Check if handle has data (non-blocking on Windows)
            # For simplicity, just try to read with a small timeout
            ready = True  # Assume ready, will handle EOF in _read_chunk_from_stdout
            time.sleep(min(0.01, remaining))  # Small sleep to avoid busy-wait
        else:
            # Unix: Use select
            import select

            elapsed = time.time() - start_time
            remaining = timeout - elapsed
            ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def _stream_without_timeout(process: Any) -> Iterator[str]:
    """Stream output without timeout (blocking I/O)."""
    if process.stdout:
        for line in process.stdout:
            yield line.rstrip()


def _cleanup_process(process: Any) -> None:
    """Ensure subprocess pipes are properly closed and process is terminated."""
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    # Make sure process is terminated
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def stream(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


# 🧱🏗️🔚
