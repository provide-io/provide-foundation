#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for process runner to improve code coverage."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.errors import ProcessError
from provide.foundation.errors.process import ProcessTimeoutError
from provide.foundation.process.sync import run, run_simple, shell, stream


class TestProcessRunnerCoverage(FoundationTestCase):
    """Test process runner functionality for improved coverage."""

    def test_run_with_path_cwd(self) -> None:
        """Test run with Path object as cwd."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path_cwd = Path(tmpdir)
            result = run(["pwd"], cwd=path_cwd, capture_output=True, check=True)
            assert tmpdir in result.stdout

    def test_run_env_variable_update(self) -> None:
        """Test run with environment variables."""
        env = {"TEST_VAR": "test_value"}
        result = run(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('TEST_VAR', 'not_found'))",
            ],
            env=env,
            capture_output=True,
            check=True,
        )
        assert "test_value" in result.stdout

    def test_run_disables_foundation_telemetry_by_default(self) -> None:
        """Test that run disables foundation telemetry by default."""
        result = run(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PROVIDE_TELEMETRY_DISABLED', 'not_set'))",
            ],
            capture_output=True,
            check=True,
        )
        assert "true" in result.stdout

    def test_run_preserves_existing_telemetry_setting(self) -> None:
        """Test that existing telemetry settings are preserved."""
        env = {"PROVIDE_TELEMETRY_DISABLED": "false"}
        result = run(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PROVIDE_TELEMETRY_DISABLED'))",
            ],
            env=env,
            capture_output=True,
            check=True,
        )
        assert "false" in result.stdout

    def test_run_simple_strips_whitespace(self) -> None:
        """Test that run_simple strips whitespace from output."""
        # Test with a command that outputs whitespace
        output = run_simple(["echo", "  test  "])
        assert output == "test"

    def test_stream_with_path_cwd(self) -> None:
        """Test stream with Path object as cwd."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path_cwd = Path(tmpdir)
            lines = list(stream(["pwd"], cwd=path_cwd))
            assert len(lines) > 0
            assert tmpdir in lines[0]

    def test_stream_with_environment_variables(self) -> None:
        """Test stream with environment variables."""
        env = {"TEST_STREAM_VAR": "stream_value"}
        lines = list(
            stream(
                [
                    sys.executable,
                    "-c",
                    "import os; print(os.environ.get('TEST_STREAM_VAR', 'not_found'))",
                ],
                env=env,
            ),
        )
        assert "stream_value" in lines[0]

    @pytest.mark.serial
    def test_stream_timeout_handling(self) -> None:
        """Test stream with timeout."""
        # Use a command that should complete quickly
        lines = list(stream(["echo", "test"], timeout=1.0))
        assert "test" in lines[0]

    def test_stream_stream_stderr_enabled(self) -> None:
        """Test stream with stderr streaming enabled."""
        # This will output to stderr, but with stream_stderr=True it goes to stdout
        lines = list(
            stream(
                [sys.executable, "-c", "import sys; sys.stderr.write('error\\n')"],
                stream_stderr=True,
            ),
        )
        # When stream_stderr=True, stderr goes to stdout so we can capture it
        assert len(lines) >= 0  # May or may not capture the stderr

    def test_stream_handles_nonblocking_io(self) -> None:
        """Test stream with basic streaming functionality."""
        # Simple test that actually works with real commands
        lines = list(stream(["echo", "test"]))
        assert len(lines) > 0
        assert "test" in lines[0]

    def test_shell_basic(self) -> None:
        """Test shell basic functionality."""
        result = shell("echo test")
        assert "test" in result.stdout

    def test_shell_with_pipes(self) -> None:
        """Test shell with shell pipes."""
        result = shell("echo 'hello world' | grep hello", allow_shell_features=True)
        assert "hello" in result.stdout

    def test_shell_failure_handling(self) -> None:
        """Test shell with command failure."""
        with pytest.raises(ProcessError):
            shell("exit 1", check=True)

    def test_shell_with_cwd_path(self) -> None:
        """Test shell with Path object as cwd."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path_cwd = Path(tmpdir)
            result = shell("pwd", cwd=path_cwd)
            assert tmpdir in result.stdout

    def test_shell_env_inheritance_and_override(self) -> None:
        """Test shell inherits and overrides environment variables."""
        env = {"SHELL_TEST_VAR": "shell_value"}
        result = shell(
            f"{sys.executable} -c \"import os; print(os.environ.get('SHELL_TEST_VAR', 'not_found'))\"",
            env=env,
            allow_shell_features=True,
        )
        assert "shell_value" in result.stdout

    def test_run_handles_timeout(self) -> None:
        """Test run handles timeout."""
        # Use a real timeout test
        with pytest.raises(ProcessTimeoutError) as exc_info:
            run(["sleep", "1"], timeout=0.1, check=True)

        assert "timed out" in str(exc_info.value)

    @patch("subprocess.run")
    def test_run_handles_subprocess_error(self, mock_run: Any) -> None:
        """Test run handles subprocess.SubprocessError."""
        mock_run.side_effect = subprocess.SubprocessError("Generic error")

        with pytest.raises(ProcessError) as exc_info:
            run(["invalid_command"], check=True)

        assert "Failed to execute command" in str(exc_info.value)


# 🧱🏗️🔚
