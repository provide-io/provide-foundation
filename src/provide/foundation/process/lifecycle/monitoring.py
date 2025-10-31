#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import asyncio

from provide.foundation.errors.process import ProcessError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import DEFAULT_PROCESS_WAIT_TIMEOUT
from provide.foundation.process.lifecycle.managed import ManagedProcess

"""Process output monitoring utilities.

This module provides async utilities for monitoring and waiting for specific
output patterns from managed processes.
"""

log = get_logger(__name__)


def _drain_remaining_output(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
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


async def _try_read_process_line(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


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

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
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
