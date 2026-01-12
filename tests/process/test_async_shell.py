#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for async_shell convenience function."""

from __future__ import annotations

import tempfile

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.aio import async_shell
from provide.foundation.process.shared import CompletedProcess

# Mark all tests in this file to run serially to avoid event loop issues
pytestmark = pytest.mark.serial


@pytest.mark.asyncio
class TestAsyncRunShell(FoundationTestCase):
    """Test async_shell function."""

    async def test_basic_shell_command(self) -> None:
        """Test basic shell command execution."""
        result = await async_shell("echo 'shell test'")

        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert "shell test" in result.stdout

    async def test_shell_with_cwd(self) -> None:
        """Test shell command with working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = await async_shell("pwd", cwd=tmpdir)

            assert tmpdir in result.stdout
            assert result.cwd == tmpdir

    async def test_shell_with_env(self) -> None:
        """Test shell command with environment."""
        custom_env = {"SHELL_TEST_VAR": "shell_value"}
        result = await async_shell("echo $SHELL_TEST_VAR", env=custom_env, allow_shell_features=True)

        assert "shell_value" in result.stdout

    async def test_shell_no_capture_output(self) -> None:
        """Test shell command without capturing output."""
        result = await async_shell("echo test", capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""
        assert result.returncode == 0

    async def test_shell_check_false(self) -> None:
        """Test shell command with check=False."""
        result = await async_shell("exit 1", check=False)

        assert result.returncode == 1

    async def test_shell_check_true_failure(self) -> None:
        """Test shell command with check=True on failure."""
        with pytest.raises(ProcessError, match="Command failed with exit code 1"):
            await async_shell("exit 1", check=True)

    async def test_shell_with_timeout(self) -> None:
        """Test shell command with timeout."""
        result = await async_shell("echo quick", timeout=5.0)

        assert result.returncode == 0
        assert "quick" in result.stdout

    async def test_shell_timeout_exceeded(self) -> None:
        """Test shell command that exceeds timeout."""
        with pytest.raises(ProcessTimeoutError, match="Command timed out after"):
            await async_shell("sleep 1", timeout=0.5)

    async def test_shell_with_kwargs(self) -> None:
        """Test shell command with additional kwargs."""
        result = await async_shell("echo kwargs", some_kwarg="value")

        assert result.returncode == 0
        assert "kwargs" in result.stdout

    async def test_shell_delegates_to_async_run(self) -> None:
        """Test that async_shell properly delegates to async_run."""
        with patch(
            "provide.foundation.process.aio.shell.async_run",
        ) as mock_run:
            mock_run.return_value = CompletedProcess(
                args=["test command"],
                returncode=0,
                stdout="test output",
                stderr="",
                cwd=None,
                env=None,
            )

            await async_shell(
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


# 🧱🏗️🔚
