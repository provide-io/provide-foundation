from __future__ import annotations

import asyncio
from collections.abc import Mapping
import functools
import os
from pathlib import Path
import subprocess
import sys
import threading
import traceback
from typing import Any

from provide.foundation.config.defaults import (
    DEFAULT_PROCESS_READCHAR_TIMEOUT,
    DEFAULT_PROCESS_READLINE_TIMEOUT,
    DEFAULT_PROCESS_TERMINATE_TIMEOUT,
    DEFAULT_PROCESS_WAIT_TIMEOUT,
)
from provide.foundation.errors.decorators import resilient
from provide.foundation.logger import get_logger
from provide.foundation.process.runner import ProcessError

"""Process lifecycle management utilities.

This module provides utilities for managing long-running subprocesses with
proper lifecycle management, monitoring, and graceful shutdown capabilities.
"""

plog = get_logger(__name__)


class ManagedProcess:
    """A managed subprocess with lifecycle support, monitoring, and graceful shutdown.

    This class wraps subprocess.Popen with additional functionality for:
    - Environment management
    - Output streaming and monitoring
    - Health checks and process monitoring
    - Graceful shutdown with timeouts
    - Background stderr relaying
    """

    def __init__(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        plog.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    @property
    def process(self) -> subprocess.Popen[bytes] | None:
        """Get the underlying subprocess.Popen instance."""
        return self._process

    @property
    def pid(self) -> int | None:
        """Get the process ID, if process is running."""
        return self._process.pid if self._process else None

    @property
    def returncode(self) -> int | None:
        """Get the return code, if process has terminated."""
        return self._process.returncode if self._process else None

    def is_running(self) -> bool:
        """Check if the process is currently running."""
        if not self._process:
            return False
        return self._process.poll() is None

    @resilient(
        error_mapper=lambda e: ProcessError(f"Failed to launch process: {e}")
        if not isinstance(e, (ProcessError, RuntimeError))
        else e,
    )
    def launch(self) -> None:
        """Launch the managed process.

        Raises:
            ProcessError: If the process fails to launch
            RuntimeError: If the process is already started

        """
        if self._started:
            raise RuntimeError("Process has already been started")

        plog.debug("🚀 Launching managed process", command=" ".join(self.command))

        self._process = subprocess.Popen(
            self.command,
            cwd=self.cwd,
            env=self._env,
            stdout=subprocess.PIPE if self.capture_output else None,
            stderr=subprocess.PIPE if self.capture_output else None,
            text=self.text_mode,
            bufsize=self.bufsize,
            **self.kwargs,
        )
        self._started = True

        plog.info(
            "🚀 Managed process started successfully",
            pid=self._process.pid,
            command=" ".join(self.command),
        )

        # Start stderr relay if enabled
        if self.stderr_relay and self._process.stderr:
            self._start_stderr_relay()

    def _start_stderr_relay(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                plog.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        plog.debug("🚀 Started stderr relay thread")

    async def read_line_async(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            plog.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def read_char_async(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            plog.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    def terminate_gracefully(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            plog.debug("Process already terminated", returncode=self._process.returncode)
            return True

        plog.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            plog.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                plog.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                plog.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    plog.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    plog.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            plog.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def cleanup(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        plog.debug("🧹 Managed process cleanup completed")

    def __enter__(self) -> ManagedProcess:
        """Context manager entry."""
        self.launch()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit with cleanup."""
        self.terminate_gracefully()
        self.cleanup()


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
                plog.debug("Read remaining output from exited process", size=len(remaining))
        except Exception:
            pass
    return buffer


def _check_pattern_found(buffer: str, expected_parts: list[str]) -> bool:
    """Check if all expected parts are found in buffer."""
    return all(part in buffer for part in expected_parts)


def _handle_process_error_exit(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    plog.error("Process exited with error", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def _handle_process_clean_exit_without_pattern(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    plog.error("Process exited without expected output", returncode=0, buffer=buffer[:200])
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
        plog.debug("Found expected pattern after process exit")
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
            plog.debug("Found expected pattern after final drain")
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
            plog.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                plog.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except Exception:
        # Process might have exited, continue
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

    plog.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            plog.debug("Process exited", returncode=last_exit_code)
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
    plog.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")
