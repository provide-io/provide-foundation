#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests to achieve full coverage for process/async_runner.py."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.aio import async_run, async_shell, async_stream


class TestAsyncInputHandling(FoundationTestCase):
    """Test async input handling and conversion for different text modes."""

    @pytest.mark.asyncio
    async def test_none_input(self) -> None:
        """Test that None input is handled correctly."""
        result = await async_run(["echo", "test"], input=None)
        assert result.returncode == 0


class TestAsyncErrorHandling(FoundationTestCase):
    """Test async error handling paths."""

    @pytest.mark.asyncio
    async def test_async_subprocess_timeout_error(self) -> None:
        """Test handling of async subprocess TimeoutError."""
        with pytest.raises(ProcessTimeoutError) as exc_info:
            await async_run(["sleep", "1"], timeout=0.01, check=True)

        assert "timed out" in str(exc_info.value).lower()

    @patch("asyncio.create_subprocess_exec")
    @pytest.mark.asyncio
    async def test_async_generic_subprocess_exception(self, mock_create: Any) -> None:
        """Test handling of generic async subprocess exceptions."""
        # Mock create_subprocess_exec to raise a generic exception
        mock_create.side_effect = OSError("Command not found")

        with pytest.raises(ProcessError) as exc_info:
            await async_run(["nonexistent_command"], check=True)

        assert "Failed to execute async command" in str(exc_info.value)
        assert exc_info.value.code == "PROCESS_ASYNC_EXECUTION_FAILED"

    @patch("asyncio.create_subprocess_exec")
    @pytest.mark.asyncio
    async def test_async_reraise_process_error(self, mock_create: Any) -> None:
        """Test that ProcessError and ProcessTimeoutError are re-raised directly."""
        # Mock create_subprocess_exec to raise a ProcessError
        original_error = ProcessError("Original error", command="test_command")
        mock_create.side_effect = original_error

        with pytest.raises(ProcessError) as exc_info:
            await async_run(["test"], check=True)

        # Should be the same exception instance
        assert exc_info.value is original_error

    @pytest.mark.asyncio
    async def test_async_command_failure_with_check_false(self) -> None:
        """Test that failed async commands don't raise when check=False."""
        result = await async_run(["false"], check=False)
        assert result.returncode != 0
        # Should not raise an exception

    @pytest.mark.asyncio
    async def test_async_command_failure_with_check_true(self) -> None:
        """Test that failed async commands raise ProcessError when check=True."""
        with pytest.raises(ProcessError) as exc_info:
            await async_run(["false"], check=True)

        assert exc_info.value.return_code != 0
        assert exc_info.value.code == "PROCESS_ASYNC_FAILED"


class TestAsyncShellExecution(FoundationTestCase):
    """Test async shell execution paths."""

    @pytest.mark.asyncio
    async def test_async_shell_with_complex_command(self) -> None:
        """Test async shell execution with complex commands."""
        result = await async_shell("echo 'hello world' | grep hello", allow_shell_features=True)

        assert result.returncode == 0
        assert "hello" in result.stdout

    @pytest.mark.asyncio
    async def test_async_shell_with_environment_variables(self) -> None:
        """Test async shell execution with custom environment."""
        result = await async_shell("echo $TEST_VAR", env={"TEST_VAR": "test_value"}, allow_shell_features=True)

        assert result.returncode == 0
        assert "test_value" in result.stdout

    @pytest.mark.asyncio
    async def test_async_shell_failure(self) -> None:
        """Test async shell command failure."""
        with pytest.raises(ProcessError):
            await async_shell("exit 1", check=True)


class TestAsyncWorkingDirectory(FoundationTestCase):
    """Test async working directory handling."""

    @pytest.mark.asyncio
    async def test_async_cwd_as_string(self, tmp_path: Any) -> None:
        """Test async working directory as string path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = await async_run(["cat", "test.txt"], cwd=str(tmp_path))

        assert result.returncode == 0
        assert "test content" in result.stdout

    @pytest.mark.asyncio
    async def test_async_cwd_as_path_object(self, tmp_path: Any) -> None:
        """Test async working directory as Path object."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = await async_run(["cat", "test.txt"], cwd=tmp_path)

        assert result.returncode == 0
        assert "test content" in result.stdout


class TestAsyncEnvironmentHandling(FoundationTestCase):
    """Test async environment variable handling."""

    @pytest.mark.asyncio
    async def test_async_env_dict_conversion(self) -> None:
        """Test that async env dict is properly converted."""
        result = await async_run(
            ["env"],
            env={"TEST_VAR": "test_value"},
            capture_output=True,
        )

        assert result.returncode == 0
        assert "TEST_VAR=test_value" in result.stdout

    @pytest.mark.asyncio
    async def test_async_env_none(self) -> None:
        """Test that None env is handled correctly in async."""
        result = await async_run(["echo", "test"], env=None)
        assert result.returncode == 0
        # Should not crash or fail


class TestAsyncStreamCommandCoverage(FoundationTestCase):
    """Test additional async stream command functionality."""

    @pytest.mark.asyncio
    async def test_async_stream_command_with_stderr(self) -> None:
        """Test async streaming command with stderr capture."""
        lines = []
        async for line in async_stream(
            [
                sys.executable,
                "-c",
                "import sys; print('stdout'); sys.stderr.write('stderr\\n')",
            ],
            stream_stderr=True,
        ):
            lines.append(line)

        # Should capture both stdout and stderr
        assert len(lines) >= 1
        output = "".join(lines)
        assert "stdout" in output or "stderr" in output

    @pytest.mark.asyncio
    async def test_async_stream_command_timeout(self) -> None:
        """Test async stream command timeout handling."""
        with pytest.raises(ProcessTimeoutError):
            # Try to stream from a long-running command with very short timeout
            # Use a command that definitely won't complete in 0.05 seconds
            lines = []
            async for line in async_stream(["sleep", "10"], timeout=0.05):
                lines.append(line)

    @patch("asyncio.create_subprocess_exec")
    @pytest.mark.asyncio
    async def test_async_stream_generic_exception(self, mock_create: Any) -> None:
        """Test async stream command with generic exception."""
        mock_create.side_effect = OSError("Command not found")

        with pytest.raises(ProcessError) as exc_info:
            lines = []
            async for line in async_stream(["nonexistent"]):
                lines.append(line)

        assert "Failed to stream async command" in str(exc_info.value)


class TestAsyncCompletedProcessConstruction(FoundationTestCase):
    """Test async CompletedProcess object construction."""

    @pytest.mark.asyncio
    async def test_async_completed_process_with_list_cmd(self) -> None:
        """Test async CompletedProcess construction with list command."""
        result = await async_run(["echo", "hello"], capture_output=True)

        assert isinstance(result.args, list)
        assert result.args == ["echo", "hello"]

    @pytest.mark.asyncio
    async def test_async_completed_process_with_string_cmd(self) -> None:
        """Test async CompletedProcess construction with string command."""
        result = await async_shell("echo hello", capture_output=True)

        # For shell commands, args might be a string
        assert "echo hello" in str(result.args)

    @pytest.mark.asyncio
    async def test_async_completed_process_without_capture(self) -> None:
        """Test async CompletedProcess when capture_output=False."""
        result = await async_run(["echo", "hello"], capture_output=False)

        # stdout/stderr should be empty strings when not captured
        assert result.stdout == ""
        assert result.stderr == ""

    @pytest.mark.asyncio
    async def test_async_completed_process_env_handling(self) -> None:
        """Test async CompletedProcess environment handling."""
        # Test with custom env
        result = await async_run(
            ["echo", "test"],
            env={"TEST_VAR": "value"},
            capture_output=True,
        )
        assert result.env is not None
        assert "TEST_VAR" in result.env

        # Test with no env
        result = await async_run(
            ["echo", "test"],
            env=None,
            capture_output=True,
        )
        assert result.env is None


class TestAsyncContextualBehavior(FoundationTestCase):
    """Test async-specific contextual behaviors."""

    @pytest.mark.asyncio
    async def test_async_cancel_during_execution(self) -> None:
        """Test that async operations can be cancelled."""
        # This tests the asyncio integration
        task = asyncio.create_task(async_run(["sleep", "10"]))

        # Give subprocess time to start to avoid cancelling during startup
        # Using 0.1s instead of 0s to prevent deadlock on cancellation during spawn
        await asyncio.sleep(0.1)

        # Cancel the task
        task.cancel()

        # Add timeout protection to prevent test hang
        # Cleanup should happen quickly (< 2s)
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(task, timeout=2.0)

    @pytest.mark.asyncio
    async def test_async_concurrent_commands(self) -> None:
        """Test running multiple async commands concurrently."""
        # Run multiple commands concurrently
        tasks = [async_run(["echo", f"hello{i}"]) for i in range(3)]

        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        for i, result in enumerate(results):
            assert result.returncode == 0
            assert f"hello{i}" in result.stdout


# 🧱🏗️🔚
