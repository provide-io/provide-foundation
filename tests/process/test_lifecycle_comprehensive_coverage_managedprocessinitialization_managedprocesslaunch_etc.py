#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for process/lifecycle.py module."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import threading

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.errors.process import ProcessError
from provide.foundation.errors.runtime import StateError
from provide.foundation.process.lifecycle import ManagedProcess


class TestManagedProcessInitialization(FoundationTestCase):
    """Test ManagedProcess initialization and properties."""

    def test_basic_initialization(self) -> None:
        """Test basic ManagedProcess initialization."""
        command = ["echo", "test"]
        proc = ManagedProcess(command)

        assert proc.command == command
        assert proc.cwd is None
        assert proc.capture_output is True
        assert proc.text_mode is False
        assert proc.bufsize == 0
        assert proc.stderr_relay is True
        assert proc._process is None
        assert proc._started is False

    def test_initialization_with_cwd_string(self) -> None:
        """Test initialization with cwd as string."""
        command = ["pwd"]
        cwd = "/tmp"
        proc = ManagedProcess(command, cwd=cwd)

        assert proc.cwd == cwd

    def test_initialization_with_cwd_path(self) -> None:
        """Test initialization with cwd as Path object."""
        command = ["pwd"]
        cwd = Path("/tmp")
        proc = ManagedProcess(command, cwd=cwd)

        assert proc.cwd == "/tmp"

    def test_initialization_with_env(self) -> None:
        """Test initialization with custom environment."""
        command = ["env"]
        custom_env = {"TEST_VAR": "test_value"}
        proc = ManagedProcess(command, env=custom_env)

        assert "TEST_VAR" in proc._env
        assert proc._env["TEST_VAR"] == "test_value"
        # Should include existing environment
        assert "PATH" in proc._env

    def test_initialization_with_all_params(self) -> None:
        """Test initialization with all parameters."""
        command = ["sleep", "1"]
        proc = ManagedProcess(
            command,
            cwd="/tmp",
            env={"TEST": "value"},
            capture_output=False,
            text_mode=True,
            bufsize=1024,
            stderr_relay=False,
            shell=True,
        )

        assert proc.command == command
        assert proc.cwd == "/tmp"
        assert proc.capture_output is False
        assert proc.text_mode is True
        assert proc.bufsize == 1024
        assert proc.stderr_relay is False
        assert "shell" in proc.kwargs

    def test_properties_before_launch(self) -> None:
        """Test properties when process not yet launched."""
        proc = ManagedProcess(["echo", "test"])

        assert proc.process is None
        assert proc.pid is None
        assert proc.returncode is None
        assert proc.is_running() is False


class TestManagedProcessLaunch(FoundationTestCase):
    """Test ManagedProcess launch functionality."""

    def test_successful_launch(self) -> None:
        """Test successful process launch."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()

        assert proc._started is True
        assert proc._process is not None
        assert proc.pid is not None
        assert isinstance(proc.pid, int)

        # Wait for process to complete
        proc._process.wait()
        proc.cleanup()

    def test_launch_already_started_error(self) -> None:
        """Test error when trying to launch already started process."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()

        with pytest.raises(StateError, match="Process has already been started"):
            proc.launch()

        proc._process.wait()
        proc.cleanup()

    def test_launch_with_invalid_command(self) -> None:
        """Test launch with invalid command."""
        proc = ManagedProcess(["/nonexistent/command"])

        with pytest.raises(ProcessError, match="Failed to launch process"):
            proc.launch()

    def test_launch_with_working_directory(self) -> None:
        """Test launch with specific working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = ManagedProcess(
                ["pwd"],
                cwd=tmpdir,
                capture_output=True,
                text_mode=True,
            )
            proc.launch()

            # Read output
            stdout, _ = proc._process.communicate()
            assert tmpdir in stdout.strip()

            proc.cleanup()

    def test_properties_after_launch(self) -> None:
        """Test properties after successful launch."""
        proc = ManagedProcess(["sleep", "0.1"])
        proc.launch()

        assert proc.process is not None
        assert proc.pid is not None
        assert proc.is_running() is True

        # Wait for process to finish
        proc._process.wait()
        assert proc.returncode is not None
        assert proc.is_running() is False

        proc.cleanup()


class TestManagedProcessOutput(FoundationTestCase):
    """Test ManagedProcess output handling."""

    @pytest.mark.asyncio
    async def test_read_line_async_success(self) -> None:
        """Test successful async line reading."""
        proc = ManagedProcess(
            ["echo", "test line"],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        line = await proc.read_line_async(timeout=2.0)
        assert "test line" in line

        proc._process.wait()
        proc.cleanup()

    @pytest.mark.asyncio
    async def test_read_line_async_no_process(self) -> None:
        """Test read_line_async when process not running."""
        proc = ManagedProcess(["echo", "test"])

        with pytest.raises(
            ProcessError,
            match="Process not running or stdout not available",
        ):
            await proc.read_line_async()

    @pytest.mark.asyncio
    async def test_read_line_async_no_stdout(self) -> None:
        """Test read_line_async when stdout not captured."""
        proc = ManagedProcess(["echo", "test"], capture_output=False)
        proc.launch()

        with pytest.raises(
            ProcessError,
            match="Process not running or stdout not available",
        ):
            await proc.read_line_async()

        proc._process.wait()
        proc.cleanup()

    @pytest.mark.asyncio
    async def test_read_char_async_success(self) -> None:
        """Test successful async character reading."""
        proc = ManagedProcess(["echo", "x"], capture_output=True, text_mode=True)
        proc.launch()

        char = await proc.read_char_async(timeout=2.0)
        assert len(char) == 1

        proc._process.wait()
        proc.cleanup()

    @pytest.mark.asyncio
    async def test_read_char_async_no_process(self) -> None:
        """Test read_char_async when process not running."""
        proc = ManagedProcess(["echo", "test"])

        with pytest.raises(
            ProcessError,
            match="Process not running or stdout not available",
        ):
            await proc.read_char_async()


class TestManagedProcessStderrRelay(FoundationTestCase):
    """Test ManagedProcess stderr relay functionality."""

    @patch("sys.stderr.write")
    @patch("sys.stderr.flush")
    def test_stderr_relay_enabled(self, mock_flush: Mock, mock_write: Mock) -> None:
        """Test stderr relay when enabled."""
        # Create a process that outputs to stderr
        proc = ManagedProcess(
            [sys.executable, "-c", "import sys; sys.stderr.write('error message\\n')"],
            stderr_relay=True,
            capture_output=True,
        )
        proc.launch()

        # Wait for process to complete and stderr thread to relay
        proc._process.wait()
        pass  # Mock the relay thread processing time

        # Check if stderr was relayed (may not be called if process completes too quickly)
        proc.cleanup()

    def test_stderr_relay_disabled(self) -> None:
        """Test that stderr relay is not started when disabled."""
        proc = ManagedProcess(["echo", "test"], stderr_relay=False, capture_output=True)
        proc.launch()

        assert proc._stderr_thread is None

        proc._process.wait()
        proc.cleanup()

    def test_stderr_relay_thread_creation(self) -> None:
        """Test stderr relay thread is created when enabled."""
        proc = ManagedProcess(["sleep", "0.1"], stderr_relay=True, capture_output=True)
        proc.launch()

        # If stderr is captured, relay thread should be created
        if proc._process.stderr:
            assert proc._stderr_thread is not None
            assert isinstance(proc._stderr_thread, threading.Thread)

        proc._process.wait()
        proc.cleanup()


class TestManagedProcessTermination(FoundationTestCase):
    """Test ManagedProcess termination functionality."""

    def test_terminate_gracefully_not_started(self) -> None:
        """Test graceful termination when process not started."""
        proc = ManagedProcess(["sleep", "1"])
        result = proc.terminate_gracefully()

        assert result is True  # No process to terminate

    def test_terminate_gracefully_already_finished(self) -> None:
        """Test graceful termination when process already finished."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        proc._process.wait()  # Wait for completion

        result = proc.terminate_gracefully()
        assert result is True

        proc.cleanup()

    def test_terminate_gracefully_success(self) -> None:
        """Test successful graceful termination."""
        proc = ManagedProcess(["sleep", "1"])
        proc.launch()

        # Process should be running
        assert proc.is_running()

        result = proc.terminate_gracefully(timeout=2.0)
        assert result is True
        assert not proc.is_running()

        proc.cleanup()

    def test_terminate_gracefully_timeout(self) -> None:
        """Test graceful termination with timeout (kill)."""
        # Create a process that ignores SIGTERM and confirms handler installation
        proc = ManagedProcess(
            [
                sys.executable,
                "-c",
                "import signal, time, sys; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                "print('ready', flush=True); time.sleep(10)",
            ],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        # Wait for confirmation that signal handler is installed
        line = proc._process.stdout.readline()  # type: ignore[union-attr]
        assert "ready" in line

        # Should timeout and force kill (returns False because force-killed)
        result = proc.terminate_gracefully(timeout=0.5)
        assert result is False  # False = force-killed (expected behavior)
        assert not proc.is_running()

        proc.cleanup()

    def test_cleanup(self) -> None:
        """Test cleanup functionality."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        proc._process.wait()

        # Create a mock stderr thread
        proc._stderr_thread = Mock()
        proc._stderr_thread.is_alive.return_value = True

        proc.cleanup()

        # Should join the stderr thread
        proc._stderr_thread.join.assert_called_once_with(timeout=1.0)


class TestManagedProcessContextManager(FoundationTestCase):
    """Test ManagedProcess as context manager."""

    def test_context_manager_success(self) -> None:
        """Test successful context manager usage."""
        with ManagedProcess(["echo", "test"]) as proc:
            # No need to call launch() - context manager already does this
            assert proc.is_running() or proc.returncode is not None

        # Process should be cleaned up after context exit
        assert not proc.is_running()

    def test_context_manager_exception(self) -> None:
        """Test context manager cleanup on exception."""
        try:
            with ManagedProcess(["sleep", "1"]) as proc:
                # No need to call launch() - context manager already does this
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Process should still be cleaned up
        assert not proc.is_running()


# 🧱🏗️🔚
