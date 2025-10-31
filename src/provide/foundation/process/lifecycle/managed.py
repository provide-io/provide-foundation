#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

from provide.foundation.errors.decorators import resilient
from provide.foundation.errors.process import ProcessError
from provide.foundation.errors.runtime import StateError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import (
    DEFAULT_PROCESS_READCHAR_TIMEOUT,
    DEFAULT_PROCESS_READLINE_TIMEOUT,
    DEFAULT_PROCESS_TERMINATE_TIMEOUT,
)

"""Managed subprocess with lifecycle support.

This module provides the ManagedProcess class for managing long-running
subprocesses with proper lifecycle management and graceful shutdown.
"""

log = get_logger(__name__)


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

        log.debug(
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
        if not isinstance(e, (ProcessError, StateError))
        else e,
    )
    def launch(self) -> None:
        """Launch the managed process.

        Raises:
            ProcessError: If the process fails to launch
            StateError: If the process is already started

        """
        if self._started:
            raise StateError(
                "Process has already been started", code="PROCESS_ALREADY_STARTED", process_state="started"
            )

        log.debug("🚀 Launching managed process", command=" ".join(self.command))

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

        log.info(
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
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

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
            log.debug("Read timeout on managed process stdout")
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
            log.debug("Character read timeout on managed process stdout")
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
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
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

        log.debug("🧹 Managed process cleanup completed")

    def __enter__(self) -> ManagedProcess:
        """Context manager entry."""
        self.launch()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit with cleanup."""
        self.terminate_gracefully()
        self.cleanup()


# 🧱🏗️🔚
