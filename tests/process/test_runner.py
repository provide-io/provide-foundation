"""Tests for subprocess runner."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from provide.foundation.errors.integration import TimeoutError
from provide.foundation.errors.process import ProcessError
from provide.foundation.process.runner import (
    run_command,
    run_shell,
    stream_command,
)


class TestRunCommand:
    """Test run_command function."""

    def test_simple_command(self) -> None:
        """Test running a simple command."""
        result = run_command(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert result.stderr == ""

    def test_command_with_args(self) -> None:
        """Test command with multiple arguments."""
        result = run_command(["echo", "hello", "world"])

        assert result.returncode == 0
        assert "hello world" in result.stdout

    def test_command_failure(self) -> None:
        """Test command that fails."""
        with pytest.raises(ProcessError) as exc_info:
            run_command(["false"], check=True)

        assert exc_info.value.return_code != 0

    def test_command_failure_no_check(self) -> None:
        """Test failed command with check=False."""
        result = run_command(["false"], check=False)

        assert result.returncode != 0

    def test_command_with_cwd(self, tmp_path: Path) -> None:
        """Test command with working directory."""
        result = run_command(["pwd"], cwd=tmp_path)

        assert str(tmp_path) in result.stdout

    def test_command_with_env(self) -> None:
        """Test command with custom environment."""
        result = run_command(
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
        result = run_command(["cat"], input=b"test input")

        assert "test input" in result.stdout

    def test_command_timeout(self) -> None:
        """Test command timeout."""
        with pytest.raises(TimeoutError):
            run_command(["sleep", "10"], timeout=0.1)

    def test_capture_output_false(self) -> None:
        """Test with capture_output=False."""
        result = run_command(["echo", "hello"], capture_output=False)

        assert result.stdout == ""
        assert result.stderr == ""

    def test_command_as_string(self) -> None:
        """Test command as string."""
        result = run_command("echo hello")

        assert result.returncode == 0
        assert "hello" in result.stdout


class TestStreamCommand:
    """Test stream_command function."""

    def test_stream_output(self) -> None:
        """Test streaming command output."""
        lines = []

        for line in stream_command(
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

        for line in stream_command(
            [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
            stream_stderr=True,
        ):
            lines.append(line)

        assert any("error" in line for line in lines)

    def test_stream_with_timeout(self) -> None:
        """Test streaming with timeout."""
        with pytest.raises(TimeoutError):
            for _ in stream_command(["sleep", "10"], timeout=0.1):
                pass


class TestRunShell:
    """Test run_shell function."""

    def test_shell_command(self) -> None:
        """Test running shell command."""
        result = run_shell("echo hello && echo world")

        assert result.returncode == 0
        assert "hello" in result.stdout
        assert "world" in result.stdout

    def test_shell_pipes(self) -> None:
        """Test shell with pipes."""
        result = run_shell("echo hello | tr a-z A-Z")

        assert "HELLO" in result.stdout

    def test_shell_failure(self) -> None:
        """Test shell command failure."""
        with pytest.raises(ProcessError):
            run_shell("exit 1", check=True)

    def test_shell_with_cwd(self, tmp_path: Path) -> None:
        """Test shell command with working directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = run_shell("cat test.txt", cwd=tmp_path)

        assert "content" in result.stdout

    def test_shell_with_env(self) -> None:
        """Test shell with environment variables."""
        result = run_shell(
            "echo $TEST_VAR",
            env={"TEST_VAR": "test_value", "PATH": "/usr/bin:/bin", "SHELL": "/bin/sh"},
        )

        assert "test_value" in result.stdout
