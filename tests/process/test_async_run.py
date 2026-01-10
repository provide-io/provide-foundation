#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for async_run command execution."""

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
from provide.foundation.process.aio import async_run
from provide.foundation.process.shared import CompletedProcess

# Mark all tests in this file to run serially to avoid event loop issues
pytestmark = pytest.mark.serial


@pytest.mark.asyncio
class TestAsyncRunCommand(FoundationTestCase):
    """Test async_run function."""

    async def test_basic_command_success(self) -> None:
        """Test successful basic command execution."""
        result = await async_run(["echo", "hello world"])

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "hello world" in result.stdout
        assert result.stderr == ""
        assert result.args == ["echo", "hello world"]

    async def test_command_with_string_cmd(self) -> None:
        """Test command execution with string command."""
        result = await async_run("echo hello", shell=True)

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "hello" in result.stdout

    async def test_command_with_cwd_string(self) -> None:
        """Test command execution with cwd as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await async_run(["pwd"], cwd=tmpdir)

            assert tmpdir in result.stdout

    async def test_command_with_cwd_path(self) -> None:
        """Test command execution with cwd as Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd_path = Path(tmpdir)
            result = await async_run(["pwd"], cwd=cwd_path)

            assert tmpdir in result.stdout
            assert result.cwd == tmpdir

    async def test_command_with_custom_env(self) -> None:
        """Test command execution with custom environment."""
        custom_env = {"TEST_ASYNC_VAR": "test_value_async"}
        result = await async_run(
            [
                sys.executable,
                "-c",
                'import os; print(f\'VAR={os.environ.get("TEST_ASYNC_VAR", "NOT_FOUND")}\')',
            ],
            env=custom_env,
        )

        assert "VAR=test_value_async" in result.stdout
        assert result.env is not None
        assert "TEST_ASYNC_VAR" in result.env

    async def test_command_env_none(self) -> None:
        """Test command execution with env=None."""
        result = await async_run(["echo", "test"], env=None)

        assert result.env is None

    async def test_command_with_input(self) -> None:
        """Test command execution with input."""
        result = await async_run(
            [
                sys.executable,
                "-c",
                "import sys; print(f'INPUT: {sys.stdin.read().strip()}')",
            ],
            input=b"test input",
        )

        assert "INPUT: test input" in result.stdout

    async def test_command_no_capture_output(self) -> None:
        """Test command execution without capturing output."""
        result = await async_run(["echo", "test"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""
        assert result.returncode == 0

    async def test_command_check_false_with_failure(self) -> None:
        """Test command execution with check=False on failing command."""
        result = await async_run(
            [sys.executable, "-c", "import sys; sys.exit(1)"],
            check=False,
        )

        assert result.returncode == 1
        # Should not raise exception when check=False

    async def test_command_check_true_with_failure(self) -> None:
        """Test command execution with check=True on failing command."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            await async_run(
                [sys.executable, "-c", "import sys; sys.exit(1)"],
                check=True,
            )

    async def test_command_with_timeout_success(self) -> None:
        """Test command execution with timeout that completes in time."""
        result = await async_run(["echo", "fast"], timeout=5.0)

        assert result.returncode == 0
        assert "fast" in result.stdout

    async def test_command_with_timeout_exceeded(self) -> None:
        """Test command execution that exceeds timeout."""
        with pytest.raises(ProcessTimeoutError, match="Command timed out after"):
            await async_run(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                timeout=0.5,
            )

    async def test_command_shell_true(self) -> None:
        """Test command execution with shell=True."""
        result = await async_run("echo 'shell command'", shell=True)

        assert result.returncode == 0
        assert "shell command" in result.stdout

    async def test_command_shell_false_list_cmd(self) -> None:
        """Test command execution with shell=False and list command."""
        result = await async_run(["echo", "no shell"])

        assert result.returncode == 0
        assert "no shell" in result.stdout

    async def test_command_with_kwargs(self) -> None:
        """Test command execution with additional kwargs."""
        # Test that kwargs are passed through (excluding 'shell')
        result = await async_run(
            ["echo", "test"],
            shell=False,
            some_kwarg="value",
        )

        assert result.returncode == 0
        assert "test" in result.stdout

    async def test_telemetry_disabled_by_default(self) -> None:
        """Test that telemetry is disabled by default in subprocess environment."""
        result = await async_run(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ],
        )

        assert "TELEMETRY=true" in result.stdout

    async def test_telemetry_env_override(self) -> None:
        """Test that custom env can override telemetry setting."""
        custom_env = {"PROVIDE_TELEMETRY_DISABLED": "false"}
        result = await async_run(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ],
            env=custom_env,
        )

        assert "TELEMETRY=false" in result.stdout

    async def test_command_execution_exception(self) -> None:
        """Test handling of command execution exceptions."""
        with pytest.raises(ProcessError, match="Failed to execute async command"):
            await async_run(["/nonexistent/command"])

    async def test_process_error_is_wrapped(self) -> None:
        """Test that a non-ProcessError is wrapped in ProcessError."""
        with (
            patch(
                "provide.foundation.process.aio.execution.create_subprocess",
                side_effect=OSError("test os error"),
            ),
            pytest.raises(ProcessError) as exc_info,
        ):
            await async_run(["echo", "test"])

        assert isinstance(exc_info.value.__cause__, OSError)

    async def test_timeout_error_is_wrapped(self) -> None:
        """Test that a non-ProcessError TimeoutError is wrapped in ProcessError."""
        with (
            patch(
                "provide.foundation.process.aio.execution.create_subprocess",
                side_effect=TimeoutError("test timeout"),
            ),
            pytest.raises(ProcessError) as exc_info,
        ):
            await async_run(["echo", "test"])

        assert isinstance(exc_info.value.__cause__, TimeoutError)


@pytest.mark.asyncio
class TestAsyncRunEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    async def test_empty_command_list(self) -> None:
        """Test execution with empty command list."""
        with pytest.raises(ProcessError):
            await async_run([])

    async def test_none_command(self) -> None:
        """Test execution with None command."""
        with pytest.raises(ProcessError):
            await async_run(None)

    async def test_mock_process_creation_failure(self) -> None:
        """Test handling of process creation failure."""
        with (
            patch(
                "asyncio.create_subprocess_exec",
                side_effect=OSError("Process creation failed"),
            ),
            pytest.raises(ProcessError, match="Failed to execute async command"),
        ):
            await async_run(["echo", "test"])

    async def test_mock_communicate_timeout(self) -> None:
        """Test timeout handling in communicate method."""
        mock_process = AsyncMock()
        mock_process.communicate = AsyncMock(side_effect=builtins.TimeoutError())
        mock_process.kill = Mock()  # Use regular Mock to avoid coroutine warnings
        mock_process.wait = AsyncMock()

        with (
            patch("asyncio.create_subprocess_exec", return_value=mock_process),
            patch("asyncio.wait_for", side_effect=builtins.TimeoutError()),
            pytest.raises(ProcessTimeoutError, match="Command timed out after"),
        ):
            await async_run(["echo", "test"], timeout=1.0)

        mock_process.kill.assert_called_once()
        # wait() is called twice: once after kill, once in cleanup
        assert mock_process.wait.call_count == 2

    async def test_decode_error_handling(self) -> None:
        """Test handling of decode errors in output."""
        # Mock process with invalid UTF-8 bytes
        mock_process = Mock()

        # Use async function instead of AsyncMock to avoid coroutine warnings
        async def mock_communicate(input: bytes | None = None) -> tuple[bytes, bytes]:
            return (b"\xff\xfe", b"")

        mock_process.communicate = mock_communicate
        mock_process.returncode = 0

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            result = await async_run(["echo", "test"])

            # Should handle decode with errors='replace' or similar
            assert result.returncode == 0

    async def test_shell_command_kwargs_filtering(self) -> None:
        """Test that invalid kwargs are filtered from subprocess kwargs."""
        with patch("asyncio.create_subprocess_shell") as mock_shell:
            mock_process = AsyncMock()
            mock_process.communicate = AsyncMock(return_value=(b"output", b""))
            mock_process.returncode = 0
            mock_shell.return_value = mock_process

            await async_run(
                "echo test",
                shell=True,
                extra_kwarg="value",
                encoding="utf-8",
            )

            # Verify invalid kwargs are filtered out, but valid ones are kept
            call_kwargs = mock_shell.call_args[1]
            assert "extra_kwarg" not in call_kwargs  # Invalid kwarg should be filtered
            assert "encoding" in call_kwargs  # Valid kwarg should be kept
            assert "shell" not in call_kwargs  # shell is handled separately, not passed as kwarg


# 🧱🏗️🔚
