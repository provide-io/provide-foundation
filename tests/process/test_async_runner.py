#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for async subprocess runner."""

from __future__ import annotations

from pathlib import Path
import sys

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.aio import async_run, async_shell, async_stream


class TestAsyncRunCommand(FoundationTestCase):
    """Test async_run function."""

    @pytest.mark.asyncio
    async def test_simple_command(self) -> None:
        """Test running a simple command."""
        result = await async_run(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert result.stderr == ""

    @pytest.mark.asyncio
    async def test_command_with_args(self) -> None:
        """Test command with multiple arguments."""
        result = await async_run(["echo", "hello", "world"])

        assert result.returncode == 0
        assert "hello world" in result.stdout

    @pytest.mark.asyncio
    async def test_command_failure(self) -> None:
        """Test command that fails."""
        with pytest.raises(ProcessError) as exc_info:
            await async_run(["false"], check=True)

        assert exc_info.value.return_code != 0

    @pytest.mark.asyncio
    async def test_command_failure_no_check(self) -> None:
        """Test failed command with check=False."""
        result = await async_run(["false"], check=False)

        assert result.returncode != 0

    @pytest.mark.asyncio
    async def test_command_with_cwd(self, tmp_path: Path) -> None:
        """Test command with working directory."""
        result = await async_run(["pwd"], cwd=tmp_path)

        assert str(tmp_path) in result.stdout

    @pytest.mark.asyncio
    async def test_command_with_env(self) -> None:
        """Test command with custom environment."""
        result = await async_run(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('TEST_VAR', 'not set'))",
            ],
            env={"TEST_VAR": "test_value", "PATH": "/usr/bin:/bin"},
        )

        assert "test_value" in result.stdout

    @pytest.mark.asyncio
    async def test_command_with_input(self) -> None:
        """Test command with input."""
        result = await async_run(["cat"], input=b"test input")

        assert "test input" in result.stdout

    @pytest.mark.asyncio
    async def test_command_timeout(self) -> None:
        """Test command timeout.

        KNOWN ISSUE: This test may fail in serial execution if run after time_machine tests.
        The pytest-asyncio event loop may cache frozen time.monotonic references from
        previous tests. Run with `pytest -n auto` for reliable results.
        """
        # Check if time is frozen by seeing if time.time() changes
        import time

        t1 = time.time()
        time.sleep(0.001)  # Use blocking sleep, not async
        t2 = time.time()

        if t2 == t1:
            pytest.skip(
                "Time is frozen - this test requires unfrozen time. "
                "Run with pytest -n auto or ensure time_machine tests run in separate process."
            )

        with pytest.raises(ProcessTimeoutError):
            await async_run(["sleep", "1"], timeout=0.1)

    @pytest.mark.asyncio
    async def test_capture_output_false(self) -> None:
        """Test with capture_output=False."""
        result = await async_run(["echo", "hello"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""


class TestAsyncStreamCommand(FoundationTestCase):
    """Test async_stream function."""

    @pytest.mark.asyncio
    async def test_stream_output(self) -> None:
        """Test streaming command output."""
        lines = []

        # Use a script that explicitly flushes and sleeps to ensure line-by-line output
        # The sleep gives the reader time to consume each line before the next
        script = """
import sys
import time
for i in range(3):
    print(f'line {i}')
    sys.stdout.flush()
    time.sleep(0.05)  # Give reader time to consume each line
"""
        async for line in async_stream(
            [sys.executable, "-u", "-c", script],
        ):
            lines.append(line)

        # Verify we got all 3 lines of output (may be combined or separate depending on timing)
        all_output = "\n".join(lines)
        assert "line 0" in all_output
        assert "line 1" in all_output
        assert "line 2" in all_output
        # Should get at least 1 line (worst case all combined) and at most 3+
        assert len(lines) >= 1

    @pytest.mark.asyncio
    async def test_stream_stderr(self) -> None:
        """Test streaming stderr."""
        lines = []

        async for line in async_stream(
            [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
            stream_stderr=True,
        ):
            lines.append(line)

        assert any("error" in line for line in lines)

    @pytest.mark.asyncio
    async def test_stream_with_timeout(self) -> None:
        """Test streaming with timeout."""
        with pytest.raises(ProcessTimeoutError):
            async for _ in async_stream(["sleep", "1"], timeout=0.1):
                pass


class TestAsyncRunShell(FoundationTestCase):
    """Test async_shell function."""

    @pytest.mark.asyncio
    async def test_shell_command(self) -> None:
        """Test running shell command."""
        result = await async_shell("echo hello && echo world", allow_shell_features=True)

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert "world" in result.stdout

    @pytest.mark.asyncio
    async def test_shell_pipes(self) -> None:
        """Test shell with pipes."""
        result = await async_shell("echo hello | tr a-z A-Z", allow_shell_features=True)

        assert "HELLO" in result.stdout

    @pytest.mark.asyncio
    async def test_shell_failure(self) -> None:
        """Test shell command failure."""
        with pytest.raises(ProcessError):
            await async_shell("exit 1", check=True)

    @pytest.mark.asyncio
    async def test_shell_with_cwd(self, tmp_path: Path) -> None:
        """Test shell command with working directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = await async_shell("cat test.txt", cwd=tmp_path)

        assert "content" in result.stdout


# 🧱🏗️🔚
