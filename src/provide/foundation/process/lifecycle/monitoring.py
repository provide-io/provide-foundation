#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import asyncio
import os
import select

from provide.foundation.errors.process import ProcessError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import DEFAULT_PROCESS_WAIT_TIMEOUT
from provide.foundation.process.lifecycle.managed import ManagedProcess
from provide.foundation.utils.timing import apply_timeout_factor

"""Process output monitoring utilities.

This module provides async utilities for monitoring and waiting for specific
output patterns from managed processes.
"""

log = get_logger(__name__)


def _stdout_fd(process: ManagedProcess) -> int | None:
    """Get the stdout file descriptor if available."""
    if not process._process or not process._process.stdout:
        return None

    try:
        return process._process.stdout.fileno()
    except (OSError, ValueError, AttributeError):
        return None


def _drain_remaining_output(process: ManagedProcess, buffer: str, buffer_size: int = 1024) -> str:
    """Drain any remaining output from process pipes."""
    if not process._process or not process._process.stdout:
        return buffer

    try:
        if process._process.poll() is not None:
            stdout_data, _ = process._process.communicate(timeout=1.0)
            if stdout_data:
                buffer += (
                    stdout_data if isinstance(stdout_data, str) else stdout_data.decode("utf-8", "replace")
                )
            return buffer
    except (OSError, ValueError, AttributeError, TimeoutError):
        pass

    fd = _stdout_fd(process)
    if fd is None:
        return buffer

    try:
        while True:
            ready, _, _ = select.select([fd], [], [], 0)
            if not ready:
                break
            chunk = os.read(fd, buffer_size)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")
    except (OSError, ValueError):
        # OSError: stream/file read errors
        # ValueError: invalid stream state or decoding errors
        pass

    return buffer


def _check_pattern_found(buffer: str, expected_parts: list[str]) -> bool:
    """Check if all expected parts are found in buffer."""
    return all(part in buffer for part in expected_parts)


def _handle_process_error_exit(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def _handle_process_clean_exit_without_pattern(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


async def _handle_exited_process(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


def _stdout_ready(process: ManagedProcess) -> bool:
    """Check if process stdout has data ready to read."""
    fd = _stdout_fd(process)
    if fd is None:
        return False

    try:
        ready, _, _ = select.select([fd], [], [], 0)
        return bool(ready)
    except (OSError, ValueError, AttributeError):
        # If readiness can't be determined, fall back to attempting a read.
        return True


def _read_stdout_chunk(process: ManagedProcess, buffer_size: int) -> str:
    """Read available stdout bytes without blocking."""
    if not process._process or not process._process.stdout:
        return ""

    fd = _stdout_fd(process)
    if fd is None:
        return ""

    try:
        chunk = os.read(fd, buffer_size)
    except (OSError, ValueError, AttributeError, BlockingIOError):
        return ""

    if not chunk:
        return ""

    return chunk.decode("utf-8", errors="replace")


def _start_stdout_read(
    process: ManagedProcess, loop: asyncio.AbstractEventLoop
) -> asyncio.Future[bytes] | None:
    """Start a single background readline on stdout without cancellation."""
    if not process._process or not process._process.stdout:
        return None

    return loop.run_in_executor(None, process._process.stdout.readline)


async def wait_for_process_output(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    timeout = apply_timeout_factor(timeout)
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process, fallback to char reads on timeout.
        remaining = timeout - (loop.time() - start_time)
        read_timeout = min(0.1, remaining)
        if read_timeout <= 0:
            break

        if _stdout_ready(process):
            chunk = _read_stdout_chunk(process, buffer_size=buffer_size)
            if chunk:
                buffer += chunk
                log.debug("Read output from process", chunk=chunk[:100])
                if _check_pattern_found(buffer, expected_parts):
                    log.debug("Found expected pattern in buffer")
                    return buffer
            else:
                if not process.is_running():
                    last_exit_code = process.returncode
                    return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)
        else:
            if not process.is_running():
                last_exit_code = process.returncode
                return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # Try to drain any remaining output before timing out
    buffer = _drain_remaining_output(process, buffer)
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


# 🧱🏗️🔚
