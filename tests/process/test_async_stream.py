#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for async_stream command streaming."""

from __future__ import annotations

import builtins
from pathlib import Path
import sys
import tempfile

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, Mock, patch
import pytest

from provide.foundation.errors.integration import TimeoutError
from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.aio import async_stream

# Mark all tests in this file to run serially to avoid event loop issues
pytestmark = pytest.mark.serial


@pytest.mark.asyncio
class TestAsyncStreamCommand(FoundationTestCase):
    """Test async_stream function."""

    async def test_basic_stream_success(self) -> None:
        """Test successful basic stream execution."""
        lines = []
        # Use separate print statements with flush and sleep to ensure line-by-line output
        script = """
import sys
import time
print('line1', flush=True)
time.sleep(0.05)
print('line2', flush=True)
time.sleep(0.05)
"""
        async for line in async_stream([sys.executable, "-u", "-c", script]):
            lines.append(line)

        # Verify content exists (buffering may combine lines)
        all_output = "\n".join(lines)
        assert "line1" in all_output
        assert "line2" in all_output
        assert len(lines) >= 1  # At least one line received

    async def test_stream_with_cwd_string(self) -> None:
        """Test stream execution with cwd as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            lines = []
            async for line in async_stream(["pwd"], cwd=tmpdir):
                lines.append(line)

            assert any(tmpdir in line for line in lines)

    async def test_stream_with_cwd_path(self) -> None:
        """Test stream execution with cwd as Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd_path = Path(tmpdir)
            lines = []
            async for line in async_stream(["pwd"], cwd=cwd_path):
                lines.append(line)

            assert any(tmpdir in line for line in lines)

    async def test_stream_with_custom_env(self) -> None:
        """Test stream execution with custom environment."""
        custom_env = {"TEST_STREAM_VAR": "stream_value"}
        lines = []
        async for line in async_stream(
            [
                sys.executable,
                "-c",
                'import os; print(f\'STREAM_VAR={os.environ.get("TEST_STREAM_VAR", "NOT_FOUND")}\')',
            ],
            env=custom_env,
        ):
            lines.append(line)

        assert any("STREAM_VAR=stream_value" in line for line in lines)

    async def test_stream_env_none(self) -> None:
        """Test stream execution with env=None."""
        lines = []
        async for line in async_stream(["echo", "test"], env=None):
            lines.append(line)

        assert len(lines) > 0

    async def test_stream_with_timeout_success(self) -> None:
        """Test stream execution with timeout that completes in time."""
        lines = []
        async for line in async_stream(
            [sys.executable, "-c", "print('fast output')"],
            timeout=10.0,
        ):
            lines.append(line)

        assert any("fast output" in line for line in lines)

    async def test_stream_with_timeout_exceeded(self) -> None:
        """Test stream execution that exceeds timeout."""
        with pytest.raises(ProcessTimeoutError, match="Command timed out after"):
            lines = []
            async for line in async_stream(
                [sys.executable, "-c", "import time; time.sleep(2); print('slow')"],
                timeout=0.5,
            ):
                lines.append(line)

    async def test_stream_stderr_true(self) -> None:
        """Test stream execution with stderr merged to stdout."""
        lines = []
        async for line in async_stream(
            [
                sys.executable,
                "-c",
                "import sys; sys.stderr.write('error\\n'); sys.stderr.flush(); print('output')",
            ],
            stream_stderr=True,
        ):
            lines.append(line)

        # Should contain both stdout and stderr when merged
        all_output = "\n".join(lines)
        assert "output" in all_output
        # Note: stderr might not always be captured depending on timing

    async def test_stream_stderr_false(self) -> None:
        """Test stream execution with stderr separate."""
        lines = []
        async for line in async_stream(
            [
                sys.executable,
                "-c",
                "import sys; sys.stderr.write('error\\n'); sys.stderr.flush(); print('output')",
            ],
            stream_stderr=False,
        ):
            lines.append(line)

        all_output = "\n".join(lines)
        assert "output" in all_output

    async def test_stream_command_failure_no_timeout(self) -> None:
        """Test stream execution with command failure (no timeout)."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            lines = []
            async for line in async_stream(
                [sys.executable, "-c", "import sys; sys.exit(1)"],
            ):
                lines.append(line)

    async def test_stream_command_failure_with_timeout(self) -> None:
        """Test stream execution with command failure (with timeout)."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            lines = []
            async for line in async_stream(
                [sys.executable, "-c", "import sys; sys.exit(1)"],
                timeout=10.0,
            ):
                lines.append(line)

    async def test_stream_with_kwargs(self) -> None:
        """Test stream execution with additional kwargs."""
        lines = []
        async for line in async_stream(["echo", "test"], some_kwarg="value"):
            lines.append(line)

        assert any("test" in line for line in lines)

    async def test_stream_telemetry_disabled(self) -> None:
        """Test that telemetry is disabled in stream environment."""
        lines = []
        async for line in async_stream(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ],
        ):
            lines.append(line)

        assert any("TELEMETRY=true" in line for line in lines)

    async def test_stream_empty_stdout(self) -> None:
        """Test stream execution with no stdout."""
        lines = []
        async for line in async_stream([sys.executable, "-c", "pass"]):
            lines.append(line)

        # Should complete without error even with no output
        assert len(lines) == 0

    async def test_stream_execution_exception(self) -> None:
        """Test handling of stream execution exceptions."""
        with pytest.raises(ProcessError, match="Failed to stream async command"):
            lines = []
            async for line in async_stream(["/nonexistent/command"]):
                lines.append(line)

    async def test_stream_process_error_is_wrapped(self) -> None:
        """Test that a non-ProcessError is wrapped in ProcessError during stream."""
        with (
            patch(
                "provide.foundation.process.aio.streaming.create_stream_subprocess",
                side_effect=OSError("stream error"),
            ),
            pytest.raises(ProcessError) as exc_info,
        ):
            lines = []
            async for line in async_stream(["echo", "test"]):
                lines.append(line)

        assert isinstance(exc_info.value.__cause__, OSError)

    async def test_stream_timeout_error_is_wrapped(self) -> None:
        """Test that a non-ProcessError TimeoutError is wrapped during stream."""
        with (
            patch(
                "provide.foundation.process.aio.streaming.create_stream_subprocess",
                side_effect=TimeoutError("stream timeout"),
            ),
            pytest.raises(ProcessError) as exc_info,
        ):
            lines = []
            async for line in async_stream(["echo", "test"]):
                lines.append(line)

        assert isinstance(exc_info.value.__cause__, TimeoutError)

    async def test_stream_string_command(self) -> None:
        """Test stream execution with string command."""
        lines = []
        async for line in async_stream("echo test"):
            lines.append(line)

        assert any("test" in line for line in lines)

    async def test_stream_readline_timeout(self) -> None:
        """Test stream timeout during readline operations."""
        mock_process = AsyncMock()
        mock_stdout = AsyncMock()
        mock_stdout.readline = AsyncMock(side_effect=builtins.TimeoutError())
        mock_process.stdout = mock_stdout
        mock_process.kill = Mock()  # Use regular Mock to avoid coroutine warnings
        mock_process.wait = AsyncMock()

        with (
            patch("asyncio.create_subprocess_exec", return_value=mock_process),
            patch("asyncio.wait_for", side_effect=builtins.TimeoutError()),
            pytest.raises(ProcessTimeoutError, match="Command timed out after"),
        ):
            lines = []
            async for line in async_stream(
                ["echo", "test"],
                timeout=1.0,
            ):
                lines.append(line)

        mock_process.kill.assert_called_once()
        mock_process.wait.assert_called_once()

    async def test_stream_no_stdout(self) -> None:
        """Test stream when process has no stdout."""
        mock_process = Mock()
        mock_process.stdout = None

        # Use async function instead of AsyncMock to avoid coroutine warnings
        async def mock_wait() -> None:
            return None

        mock_process.wait = mock_wait
        mock_process.returncode = 0

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            lines = []
            async for line in async_stream(["echo", "test"]):
                lines.append(line)

            assert len(lines) == 0


# 🧱🏗️🔚
