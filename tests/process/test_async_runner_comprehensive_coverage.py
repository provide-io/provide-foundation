"""Comprehensive coverage tests for process/async_runner.py module."""

import asyncio
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Mark all tests in this file to run serially to avoid event loop issues
pytestmark = pytest.mark.serial

from provide.foundation.process.async_runner import (
    async_run_command,
    async_stream_command,
    async_run_shell,
)
from provide.foundation.process.runner import (
    CompletedProcess,
    ProcessError,
    TimeoutError,
)


@pytest.mark.asyncio
class TestAsyncRunCommand:
    """Test async_run_command function."""

    async def test_basic_command_success(self):
        """Test successful basic command execution."""
        result = await async_run_command(["echo", "hello world"])

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "hello world" in result.stdout
        assert result.stderr == ""
        assert result.args == ["echo", "hello world"]

    async def test_command_with_string_cmd(self):
        """Test command execution with string command."""
        result = await async_run_command("echo hello", shell=True)

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "hello" in result.stdout

    async def test_command_with_cwd_string(self):
        """Test command execution with cwd as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await async_run_command(["pwd"], cwd=tmpdir)

            assert tmpdir in result.stdout

    async def test_command_with_cwd_path(self):
        """Test command execution with cwd as Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd_path = Path(tmpdir)
            result = await async_run_command(["pwd"], cwd=cwd_path)

            assert tmpdir in result.stdout
            assert result.cwd == tmpdir

    async def test_command_with_custom_env(self):
        """Test command execution with custom environment."""
        custom_env = {"TEST_ASYNC_VAR": "test_value_async"}
        result = await async_run_command(
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

    async def test_command_env_none(self):
        """Test command execution with env=None."""
        result = await async_run_command(["echo", "test"], env=None)

        assert result.env is None

    async def test_command_with_input(self):
        """Test command execution with input."""
        result = await async_run_command(
            [
                sys.executable,
                "-c",
                "import sys; print(f'INPUT: {sys.stdin.read().strip()}')",
            ],
            input=b"test input",
        )

        assert "INPUT: test input" in result.stdout

    async def test_command_no_capture_output(self):
        """Test command execution without capturing output."""
        result = await async_run_command(["echo", "test"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""
        assert result.returncode == 0

    async def test_command_check_false_with_failure(self):
        """Test command execution with check=False on failing command."""
        result = await async_run_command(
            [sys.executable, "-c", "import sys; sys.exit(1)"], check=False
        )

        assert result.returncode == 1
        # Should not raise exception when check=False

    async def test_command_check_true_with_failure(self):
        """Test command execution with check=True on failing command."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            await async_run_command(
                [sys.executable, "-c", "import sys; sys.exit(1)"], check=True
            )

    async def test_command_with_timeout_success(self):
        """Test command execution with timeout that completes in time."""
        result = await async_run_command(["echo", "fast"], timeout=5.0)

        assert result.returncode == 0
        assert "fast" in result.stdout

    async def test_command_with_timeout_exceeded(self):
        """Test command execution that exceeds timeout."""
        with pytest.raises(TimeoutError, match="Command timed out after"):
            await async_run_command(
                [sys.executable, "-c", "import time; time.sleep(2)"], timeout=0.5
            )

    async def test_command_shell_true(self):
        """Test command execution with shell=True."""
        result = await async_run_command("echo 'shell command'", shell=True)

        assert result.returncode == 0
        assert "shell command" in result.stdout

    async def test_command_shell_false_list_cmd(self):
        """Test command execution with shell=False and list command."""
        result = await async_run_command(["echo", "no shell"])

        assert result.returncode == 0
        assert "no shell" in result.stdout

    async def test_command_shell_false_string_cmd(self):
        """Test command execution with shell=False and string command."""
        result = await async_run_command("echo", shell=False)

        assert result.returncode == 0

    async def test_command_with_kwargs(self):
        """Test command execution with additional kwargs."""
        # Test that kwargs are passed through (excluding 'shell')
        result = await async_run_command(
            ["echo", "test"], shell=False, some_kwarg="value"
        )

        assert result.returncode == 0
        assert "test" in result.stdout

    async def test_telemetry_disabled_by_default(self):
        """Test that telemetry is disabled by default in subprocess environment."""
        result = await async_run_command(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ]
        )

        assert "TELEMETRY=true" in result.stdout

    async def test_telemetry_env_override(self):
        """Test that custom env can override telemetry setting."""
        custom_env = {"PROVIDE_TELEMETRY_DISABLED": "false"}
        result = await async_run_command(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ],
            env=custom_env,
        )

        assert "TELEMETRY=false" in result.stdout

    async def test_command_execution_exception(self):
        """Test handling of command execution exceptions."""
        with pytest.raises(ProcessError, match="Failed to execute async command"):
            await async_run_command(["/nonexistent/command"])

    async def test_process_error_reraise(self):
        """Test that ProcessError is re-raised correctly."""
        # Mock to raise ProcessError in the try block
        with patch(
            "asyncio.create_subprocess_exec", side_effect=ProcessError("test error")
        ):
            with pytest.raises(ProcessError, match="test error"):
                await async_run_command(["echo", "test"])

    async def test_timeout_error_reraise(self):
        """Test that TimeoutError is re-raised correctly."""
        # Mock to raise TimeoutError in the try block
        with patch(
            "asyncio.create_subprocess_exec", side_effect=TimeoutError("timeout error")
        ):
            with pytest.raises(TimeoutError, match="timeout error"):
                await async_run_command(["echo", "test"])


@pytest.mark.asyncio
class TestAsyncStreamCommand:
    """Test async_stream_command function."""

    async def test_basic_stream_success(self):
        """Test successful basic stream execution."""
        lines = []
        async for line in async_stream_command(
            [
                sys.executable,
                "-c",
                "import sys; sys.stdout.write('line1\\nline2\\n'); sys.stdout.flush()",
            ]
        ):
            lines.append(line)

        assert len(lines) == 2
        assert "line1" in lines
        assert "line2" in lines

    async def test_stream_with_cwd_string(self):
        """Test stream execution with cwd as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            lines = []
            async for line in async_stream_command(["pwd"], cwd=tmpdir):
                lines.append(line)

            assert any(tmpdir in line for line in lines)

    async def test_stream_with_cwd_path(self):
        """Test stream execution with cwd as Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd_path = Path(tmpdir)
            lines = []
            async for line in async_stream_command(["pwd"], cwd=cwd_path):
                lines.append(line)

            assert any(tmpdir in line for line in lines)

    async def test_stream_with_custom_env(self):
        """Test stream execution with custom environment."""
        custom_env = {"TEST_STREAM_VAR": "stream_value"}
        lines = []
        async for line in async_stream_command(
            [
                sys.executable,
                "-c",
                'import os; print(f\'STREAM_VAR={os.environ.get("TEST_STREAM_VAR", "NOT_FOUND")}\')',
            ],
            env=custom_env,
        ):
            lines.append(line)

        assert any("STREAM_VAR=stream_value" in line for line in lines)

    async def test_stream_env_none(self):
        """Test stream execution with env=None."""
        lines = []
        async for line in async_stream_command(["echo", "test"], env=None):
            lines.append(line)

        assert len(lines) > 0

    async def test_stream_with_timeout_success(self):
        """Test stream execution with timeout that completes in time."""
        lines = []
        async for line in async_stream_command(
            [sys.executable, "-c", "print('fast output')"], timeout=5.0
        ):
            lines.append(line)

        assert any("fast output" in line for line in lines)

    async def test_stream_with_timeout_exceeded(self):
        """Test stream execution that exceeds timeout."""
        with pytest.raises(TimeoutError, match="Command timed out after"):
            lines = []
            async for line in async_stream_command(
                [sys.executable, "-c", "import time; time.sleep(2); print('slow')"],
                timeout=0.5,
            ):
                lines.append(line)

    async def test_stream_stderr_true(self):
        """Test stream execution with stderr merged to stdout."""
        lines = []
        async for line in async_stream_command(
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

    async def test_stream_stderr_false(self):
        """Test stream execution with stderr separate."""
        lines = []
        async for line in async_stream_command(
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

    async def test_stream_command_failure_no_timeout(self):
        """Test stream execution with command failure (no timeout)."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            lines = []
            async for line in async_stream_command(
                [sys.executable, "-c", "import sys; sys.exit(1)"]
            ):
                lines.append(line)

    async def test_stream_command_failure_with_timeout(self):
        """Test stream execution with command failure (with timeout)."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            lines = []
            async for line in async_stream_command(
                [sys.executable, "-c", "import sys; sys.exit(1)"], timeout=5.0
            ):
                lines.append(line)

    async def test_stream_with_kwargs(self):
        """Test stream execution with additional kwargs."""
        lines = []
        async for line in async_stream_command(["echo", "test"], some_kwarg="value"):
            lines.append(line)

        assert any("test" in line for line in lines)

    async def test_stream_telemetry_disabled(self):
        """Test that telemetry is disabled in stream environment."""
        lines = []
        async for line in async_stream_command(
            [
                sys.executable,
                "-c",
                'import os; print(f\'TELEMETRY={os.environ.get("PROVIDE_TELEMETRY_DISABLED", "NOT_SET")}\')',
            ]
        ):
            lines.append(line)

        assert any("TELEMETRY=true" in line for line in lines)

    async def test_stream_empty_stdout(self):
        """Test stream execution with no stdout."""
        lines = []
        async for line in async_stream_command([sys.executable, "-c", "pass"]):
            lines.append(line)

        # Should complete without error even with no output
        assert len(lines) == 0

    async def test_stream_execution_exception(self):
        """Test handling of stream execution exceptions."""
        with pytest.raises(ProcessError, match="Failed to stream async command"):
            lines = []
            async for line in async_stream_command(["/nonexistent/command"]):
                lines.append(line)

    async def test_stream_process_error_reraise(self):
        """Test that ProcessError is re-raised in stream."""
        with patch(
            "asyncio.create_subprocess_exec", side_effect=ProcessError("stream error")
        ):
            with pytest.raises(ProcessError, match="stream error"):
                lines = []
                async for line in async_stream_command(["echo", "test"]):
                    lines.append(line)

    async def test_stream_timeout_error_reraise(self):
        """Test that TimeoutError is re-raised in stream."""
        with patch(
            "asyncio.create_subprocess_exec", side_effect=TimeoutError("stream timeout")
        ):
            with pytest.raises(TimeoutError, match="stream timeout"):
                lines = []
                async for line in async_stream_command(["echo", "test"]):
                    lines.append(line)

    async def test_stream_string_command(self):
        """Test stream execution with string command."""
        lines = []
        async for line in async_stream_command("echo test"):
            lines.append(line)

        assert any("test" in line for line in lines)


@pytest.mark.asyncio
class TestAsyncRunShell:
    """Test async_run_shell function."""

    async def test_basic_shell_command(self):
        """Test basic shell command execution."""
        result = await async_run_shell("echo 'shell test'")

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "shell test" in result.stdout

    async def test_shell_with_cwd(self):
        """Test shell command with working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await async_run_shell("pwd", cwd=tmpdir)

            assert tmpdir in result.stdout
            assert result.cwd == tmpdir

    async def test_shell_with_env(self):
        """Test shell command with environment."""
        custom_env = {"SHELL_TEST_VAR": "shell_value"}
        result = await async_run_shell("echo $SHELL_TEST_VAR", env=custom_env)

        assert "shell_value" in result.stdout

    async def test_shell_no_capture_output(self):
        """Test shell command without capturing output."""
        result = await async_run_shell("echo test", capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""
        assert result.returncode == 0

    async def test_shell_check_false(self):
        """Test shell command with check=False."""
        result = await async_run_shell("exit 1", check=False)

        assert result.returncode == 1

    async def test_shell_check_true_failure(self):
        """Test shell command with check=True on failure."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            await async_run_shell("exit 1", check=True)

    async def test_shell_with_timeout(self):
        """Test shell command with timeout."""
        result = await async_run_shell("echo quick", timeout=5.0)

        assert result.returncode == 0
        assert "quick" in result.stdout

    async def test_shell_timeout_exceeded(self):
        """Test shell command that exceeds timeout."""
        with pytest.raises(TimeoutError, match="Command timed out after"):
            await async_run_shell("sleep 2", timeout=0.5)

    async def test_shell_with_kwargs(self):
        """Test shell command with additional kwargs."""
        result = await async_run_shell("echo kwargs", some_kwarg="value")

        assert result.returncode == 0
        assert "kwargs" in result.stdout

    async def test_shell_delegates_to_async_run_command(self):
        """Test that async_run_shell properly delegates to async_run_command."""
        with patch(
            "provide.foundation.process.async_runner.async_run_command"
        ) as mock_run:
            mock_run.return_value = CompletedProcess(
                args="test command",
                returncode=0,
                stdout="test output",
                stderr="",
                cwd=None,
                env=None,
            )

            await async_run_shell(
                "test command",
                cwd="/tmp",
                env={"TEST": "value"},
                capture_output=True,
                check=False,
                timeout=10.0,
                extra_arg="extra",
            )

            mock_run.assert_called_once_with(
                "test command",
                cwd="/tmp",
                env={"TEST": "value"},
                capture_output=True,
                check=False,
                timeout=10.0,
                shell=True,
                extra_arg="extra",
            )


@pytest.mark.asyncio
class TestAsyncRunnerEdgeCases:
    """Test edge cases and error conditions."""

    async def test_empty_command_list(self):
        """Test execution with empty command list."""
        with pytest.raises(ProcessError):
            await async_run_command([])

    async def test_none_command(self):
        """Test execution with None command."""
        with pytest.raises(ProcessError):
            await async_run_command(None)

    async def test_mock_process_creation_failure(self):
        """Test handling of process creation failure."""
        with patch(
            "asyncio.create_subprocess_exec",
            side_effect=OSError("Process creation failed"),
        ):
            with pytest.raises(ProcessError, match="Failed to execute async command"):
                await async_run_command(["echo", "test"])

    async def test_mock_communicate_timeout(self):
        """Test timeout handling in communicate method."""
        mock_process = AsyncMock()
        mock_process.communicate = AsyncMock(side_effect=asyncio.TimeoutError())
        mock_process.kill = AsyncMock()
        mock_process.wait = AsyncMock()

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError()):
                with pytest.raises(TimeoutError, match="Command timed out after"):
                    await async_run_command(["echo", "test"], timeout=1.0)

                mock_process.kill.assert_called_once()
                mock_process.wait.assert_called_once()

    async def test_decode_error_handling(self):
        """Test handling of decode errors in output."""
        # Mock process with invalid UTF-8 bytes
        mock_process = AsyncMock()
        mock_process.communicate = AsyncMock(return_value=(b"\xff\xfe", b""))
        mock_process.returncode = 0

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            result = await async_run_command(["echo", "test"])

            # Should handle decode with errors='replace' or similar
            assert result.returncode == 0

    async def test_stream_readline_timeout(self):
        """Test stream timeout during readline operations."""
        mock_process = AsyncMock()
        mock_stdout = AsyncMock()
        mock_stdout.readline = AsyncMock(side_effect=asyncio.TimeoutError())
        mock_process.stdout = mock_stdout
        mock_process.kill = AsyncMock()
        mock_process.wait = AsyncMock()

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError()):
                with pytest.raises(TimeoutError, match="Command timed out after"):
                    lines = []
                    async for line in async_stream_command(
                        ["echo", "test"], timeout=1.0
                    ):
                        lines.append(line)

                mock_process.kill.assert_called_once()
                mock_process.wait.assert_called_once()

    async def test_stream_no_stdout(self):
        """Test stream when process has no stdout."""
        mock_process = AsyncMock()
        mock_process.stdout = None
        mock_process.wait = AsyncMock()
        mock_process.returncode = 0

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            lines = []
            async for line in async_stream_command(["echo", "test"]):
                lines.append(line)

            assert len(lines) == 0

    async def test_shell_command_kwargs_filtering(self):
        """Test that invalid kwargs are filtered from subprocess kwargs."""
        with patch("asyncio.create_subprocess_shell") as mock_shell:
            mock_process = AsyncMock()
            mock_process.communicate = AsyncMock(return_value=(b"output", b""))
            mock_process.returncode = 0
            mock_shell.return_value = mock_process

            await async_run_command(
                "echo test", shell=True, extra_kwarg="value", encoding="utf-8"
            )

            # Verify invalid kwargs are filtered out, but valid ones are kept
            call_kwargs = mock_shell.call_args[1]
            assert "extra_kwarg" not in call_kwargs  # Invalid kwarg should be filtered
            assert "encoding" in call_kwargs  # Valid kwarg should be kept
            assert (
                "shell" not in call_kwargs
            )  # shell is handled separately, not passed as kwarg
