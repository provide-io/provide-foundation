#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for process/lifecycle.py module."""

from __future__ import annotations

import sys
from typing import Any, Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.errors.process import ProcessError
from provide.foundation.process.lifecycle import ManagedProcess, wait_for_process_output

pytestmark = pytest.mark.xdist_group(name="process_lifecycle_serial")


class TestManagedProcessEdgeCases(FoundationTestCase):
    """Test ManagedProcess edge cases and error conditions."""

    def test_is_running_no_process(self) -> None:
        """Test is_running when no process exists."""
        proc = ManagedProcess(["echo", "test"])
        assert proc.is_running() is False

    def test_launch_with_shell_kwarg(self) -> None:
        """Test launch with shell=True kwarg."""
        if sys.platform != "win32":
            proc = ManagedProcess(["echo test"], shell=True)
            proc.launch()

            proc._process.wait()
            assert proc.returncode == 0

            proc.cleanup()

    @patch("subprocess.Popen")
    def test_launch_subprocess_exception(self, mock_popen: Mock) -> None:
        """Test launch when subprocess.Popen raises exception."""
        mock_popen.side_effect = OSError("Permission denied")

        proc = ManagedProcess(["echo", "test"])
        with pytest.raises(ProcessError, match="Failed to launch process"):
            proc.launch()

    def test_stderr_relay_no_stderr(self) -> None:
        """Test stderr relay when no stderr pipe."""
        proc = ManagedProcess(["echo", "test"], capture_output=False)
        proc.launch()

        # Should not create stderr thread when no stderr pipe
        assert proc._stderr_thread is None

        proc._process.wait()
        proc.cleanup()

    def test_start_stderr_relay_no_process(self) -> None:
        """Test _start_stderr_relay when no process."""
        proc = ManagedProcess(["echo", "test"])
        proc._start_stderr_relay()  # Should not crash

        assert proc._stderr_thread is None


class TestWaitForProcessOutput(FoundationTestCase):
    """Test wait_for_process_output function."""

    @pytest.mark.asyncio
    async def test_wait_for_output_success(self) -> None:
        """Test successful output waiting."""
        proc = ManagedProcess(
            [
                sys.executable,
                "-u",
                "-c",
                (
                    "import sys, time; "
                    "print('start', flush=True); "
                    "print('middle', flush=True); "
                    "print('end', flush=True); "
                    "time.sleep(3)"
                ),
            ],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        result = await wait_for_process_output(
            proc,
            expected_parts=["start", "middle", "end"],
            timeout=10.0,
        )

        assert "start" in result
        assert "middle" in result
        assert "end" in result

        proc._process.wait()
        proc.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_output_timeout(self) -> None:
        """Test timeout when expected output never comes."""
        proc = ManagedProcess(
            [sys.executable, "-c", "import time; time.sleep(2)"],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        with pytest.raises(TimeoutError, match=r"Expected pattern .* not found within"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=1.0,
            )

        proc.terminate_gracefully()
        proc.cleanup()

    @pytest.mark.asyncio
    async def test_wait_for_output_process_exits(self) -> None:
        """Test when process exits before expected output."""
        proc = ManagedProcess(
            [sys.executable, "-c", "import sys; sys.exit(1)"],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        with pytest.raises(ProcessError, match="Process exited with code 1"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=10.0,
            )

        proc.cleanup()

    async def test_wait_for_output_char_fallback(self) -> None:
        """Test character-by-character fallback when line reading times out."""
        # Mock the read_line_async to raise TimeoutError
        proc = ManagedProcess(
            [
                sys.executable,
                "-c",
                "import sys; sys.stdout.write('a'); sys.stdout.flush()",
            ],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        # Mock read_line_async to timeout but read_char_async to succeed
        original_read_line = proc.read_line_async
        original_read_char = proc.read_char_async

        async def mock_read_line(*args: Any, **kwargs: Any) -> Never:
            raise TimeoutError

        proc.read_line_async = mock_read_line

        result = await wait_for_process_output(proc, expected_parts=["a"], timeout=6.0)

        assert "a" in result

        # Restore original methods
        proc.read_line_async = original_read_line
        proc.read_char_async = original_read_char

        proc._process.wait()
        proc.cleanup()

    async def test_wait_for_output_both_timeouts(self) -> None:
        """Test when both line and char reading timeout."""
        # Use a longer-running process that won't exit before timeout
        proc = ManagedProcess(
            [sys.executable, "-c", "import time; time.sleep(10)"],
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        # Mock both reading methods to timeout
        async def mock_timeout(*args: Any, **kwargs: Any) -> Never:
            raise TimeoutError

        proc.read_line_async = mock_timeout
        proc.read_char_async = mock_timeout

        with pytest.raises(TimeoutError, match=r"Expected pattern .* not found within"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=0.5,  # Short timeout to ensure test completes quickly
            )

        proc.terminate_gracefully()
        proc.cleanup()


@pytest.mark.serial  # These tests have timing issues with parallel execution
class TestProcessLifecycleIntegration(FoundationTestCase):
    """Integration tests for process lifecycle functionality."""

    def test_full_lifecycle_simple_command(self) -> None:
        """Test full lifecycle with simple command."""
        with ManagedProcess(["echo", "hello world"]) as proc:
            # No need to call launch() - context manager already does this
            assert proc.is_running() or proc.returncode is not None

        # Should be cleaned up after context exit
        assert not proc.is_running()

    @pytest.mark.asyncio
    async def test_full_lifecycle_with_output_waiting(self) -> None:
        """Test full lifecycle with output waiting."""
        with ManagedProcess(
            [
                sys.executable,
                "-u",
                "-c",
                "import sys; print('ready', flush=True); import time; time.sleep(5)",
            ],
            capture_output=True,
            text_mode=True,
        ) as proc:
            # No need to call launch() - context manager already does this

            # Wait for ready signal
            result = await wait_for_process_output(proc, ["ready"], timeout=10.0)
            assert "ready" in result

            # Terminate the process (since it's waiting for input)
            proc.terminate_gracefully()

    def test_environment_inheritance(self) -> None:
        """Test that custom environment is properly inherited."""
        custom_env = {"TEST_PROCESS_VAR": "test_value_12345"}

        proc = ManagedProcess(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TEST_VAR={os.environ.get("TEST_PROCESS_VAR", "NOT_FOUND")}\')',
            ],
            env=custom_env,
            capture_output=True,
            text_mode=True,
        )
        proc.launch()

        stdout, _ = proc._process.communicate()
        assert "TEST_VAR=test_value_12345" in stdout

        proc.cleanup()


# 🧱🏗️🔚
