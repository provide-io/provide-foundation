#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for subprocess runner."""

from __future__ import annotations

from pathlib import Path
import sys

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.process.sync import run, shell, stream


class TestRunCommand(FoundationTestCase):
    """Test run_command function."""

    def test_simple_command(self) -> None:
        """Test running a simple command."""
        result = run(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert result.stderr == ""

    def test_command_with_args(self) -> None:
        """Test command with multiple arguments."""
        result = run(["echo", "hello", "world"])

        assert result.returncode == 0
        assert "hello world" in result.stdout

    def test_command_failure(self) -> None:
        """Test command that fails."""
        with pytest.raises(ProcessError) as exc_info:
            run(["false"], check=True)

        assert exc_info.value.return_code != 0

    def test_command_failure_no_check(self) -> None:
        """Test failed command with check=False."""
        result = run(["false"], check=False)

        assert result.returncode != 0

    def test_command_with_cwd(self, tmp_path: Path) -> None:
        """Test command with working directory."""
        result = run(["pwd"], cwd=tmp_path)

        assert str(tmp_path) in result.stdout

    def test_command_with_env(self) -> None:
        """Test command with custom environment."""
        result = run(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('TEST_VAR', 'not set'))",
            ],
            env={"TEST_VAR": "test_value", "PATH": "/usr/bin:/bin"},
        )

        assert "test_value" in result.stdout

    def test_command_with_input(self) -> None:
        """Test command with input."""
        result = run(["cat"], input=b"test input")

        assert "test input" in result.stdout

    def test_command_timeout(self) -> None:
        """Test command timeout."""
        with pytest.raises(ProcessTimeoutError):
            run(["sleep", "1"], timeout=0.1)

    def test_capture_output_false(self) -> None:
        """Test with capture_output=False."""
        result = run(["echo", "hello"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""

    def test_command_as_string(self) -> None:
        """Test command as string requires explicit shell=True."""
        result = run("echo hello", shell=True)

        assert result.returncode == 0
        assert "hello" in result.stdout


class TestStreamCommand(FoundationTestCase):
    """Test stream_command function."""

    def test_stream_output(self) -> None:
        """Test streaming command output."""
        lines = []

        for line in stream(
            [sys.executable, "-c", "for i in range(3): print(f'line {i}')"],
        ):
            lines.append(line)

        assert len(lines) == 3
        assert "line 0" in lines[0]
        assert "line 1" in lines[1]
        assert "line 2" in lines[2]

    def test_stream_stderr(self) -> None:
        """Test streaming stderr."""
        lines = []

        for line in stream(
            [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
            stream_stderr=True,
        ):
            lines.append(line)

        assert any("error" in line for line in lines)

    def test_stream_with_timeout(self) -> None:
        """Test streaming with timeout."""
        with pytest.raises(ProcessTimeoutError):
            for _ in stream(["sleep", "1"], timeout=0.1):
                pass


class TestRunShell(FoundationTestCase):
    """Test run_shell function."""

    def test_shell_command(self) -> None:
        """Test running shell command."""
        result = shell("echo hello && echo world", allow_shell_features=True)

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert "world" in result.stdout

    def test_shell_pipes(self) -> None:
        """Test shell with pipes."""
        result = shell("echo hello | tr a-z A-Z", allow_shell_features=True)

        assert "HELLO" in result.stdout

    def test_shell_failure(self) -> None:
        """Test shell command failure."""
        with pytest.raises(ProcessError):
            shell("exit 1", check=True)

    def test_shell_with_cwd(self, tmp_path: Path) -> None:
        """Test shell command with working directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = shell("cat test.txt", cwd=tmp_path)

        assert "content" in result.stdout

    def test_shell_with_env(self) -> None:
        """Test shell with environment variables."""
        result = shell(
            "echo $TEST_VAR",
            env={"TEST_VAR": "test_value", "PATH": "/usr/bin:/bin", "SHELL": "/bin/sh"},
            allow_shell_features=True,
        )

        assert "test_value" in result.stdout


# 🧱🏗️🔚
