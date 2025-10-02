"""Tests for async subprocess runner."""

from __future__ import annotations

from pathlib import Path
import sys

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.async_runner import (
    async_run_command,
    async_run_shell,
    async_stream_command,
)


class TestAsyncRunCommand(FoundationTestCase):
    """Test async_run_command function."""

    @pytest.mark.asyncio
    async def test_simple_command(self) -> None:
        """Test running a simple command."""
        result = await async_run_command(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert result.stderr == ""

    @pytest.mark.asyncio
    async def test_command_with_args(self) -> None:
        """Test command with multiple arguments."""
        result = await async_run_command(["echo", "hello", "world"])

        assert result.returncode == 0
        assert "hello world" in result.stdout

    @pytest.mark.asyncio
    async def test_command_failure(self) -> None:
        """Test command that fails."""
        with pytest.raises(ProcessError) as exc_info:
            await async_run_command(["false"], check=True)

        assert exc_info.value.return_code != 0

    @pytest.mark.asyncio
    async def test_command_failure_no_check(self) -> None:
        """Test failed command with check=False."""
        result = await async_run_command(["false"], check=False)

        assert result.returncode != 0

    @pytest.mark.asyncio
    async def test_command_with_cwd(self, tmp_path: Path) -> None:
        """Test command with working directory."""
        result = await async_run_command(["pwd"], cwd=tmp_path)

        assert str(tmp_path) in result.stdout

    @pytest.mark.asyncio
    async def test_command_with_env(self) -> None:
        """Test command with custom environment."""
        result = await async_run_command(
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
        result = await async_run_command(["cat"], input=b"test input")

        assert "test input" in result.stdout

    @pytest.mark.asyncio
    @pytest.mark.xdist_group(name="timeout_tests")
    async def test_command_timeout(self) -> None:
        """Test command timeout.

        NOTE: This test is grouped with xdist to ensure it runs on a worker that hasn't
        run time_machine tests, which can leave frozen time references in event loops.
        """
        with pytest.raises(ProcessTimeoutError):
            await async_run_command(["sleep", "1"], timeout=0.1)

    @pytest.mark.asyncio
    async def test_capture_output_false(self) -> None:
        """Test with capture_output=False."""
        result = await async_run_command(["echo", "hello"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""


class TestAsyncStreamCommand(FoundationTestCase):
    """Test async_stream_command function."""

    @pytest.mark.asyncio
    async def test_stream_output(self) -> None:
        """Test streaming command output."""
        lines = []

        async for line in async_stream_command(
            [sys.executable, "-c", "for i in range(3): print(f'line {i}')"],
        ):
            lines.append(line)

        assert len(lines) == 3
        assert "line 0" in lines[0]
        assert "line 1" in lines[1]
        assert "line 2" in lines[2]

    @pytest.mark.asyncio
    async def test_stream_stderr(self) -> None:
        """Test streaming stderr."""
        lines = []

        async for line in async_stream_command(
            [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
            stream_stderr=True,
        ):
            lines.append(line)

        assert any("error" in line for line in lines)

    @pytest.mark.asyncio
    async def test_stream_with_timeout(self) -> None:
        """Test streaming with timeout."""
        with pytest.raises(ProcessTimeoutError):
            async for _ in async_stream_command(["sleep", "1"], timeout=0.1):
                pass


class TestAsyncRunShell(FoundationTestCase):
    """Test async_run_shell function."""

    @pytest.mark.asyncio
    async def test_shell_command(self) -> None:
        """Test running shell command."""
        result = await async_run_shell("echo hello && echo world")

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert "world" in result.stdout

    @pytest.mark.asyncio
    async def test_shell_pipes(self) -> None:
        """Test shell with pipes."""
        result = await async_run_shell("echo hello | tr a-z A-Z")

        assert "HELLO" in result.stdout

    @pytest.mark.asyncio
    async def test_shell_failure(self) -> None:
        """Test shell command failure."""
        with pytest.raises(ProcessError):
            await async_run_shell("exit 1", check=True)

    @pytest.mark.asyncio
    async def test_shell_with_cwd(self, tmp_path: Path) -> None:
        """Test shell command with working directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = await async_run_shell("cat test.txt", cwd=tmp_path)

        assert "content" in result.stdout
