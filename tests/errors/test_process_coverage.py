#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for errors/process.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.errors.process import (
    CommandNotFoundError,
    ProcessError,
    ProcessTimeoutError,
)


class TestProcessError(FoundationTestCase):
    """Test ProcessError class comprehensively."""

    def test_basic_process_error(self) -> None:
        """Test basic ProcessError initialization."""
        error = ProcessError("Process failed")

        assert str(error) == "Process failed"
        assert error.command is None
        assert error.return_code is None
        assert error.stdout is None
        assert error.stderr is None
        assert error.timeout is False
        assert error._default_code() == "PROCESS_ERROR"

    def test_process_error_with_command_string(self) -> None:
        """Test ProcessError with string command."""
        error = ProcessError("Command failed", command="ls -la", return_code=1)

        expected_message = "Command failed\nCommand: ls -la\nReturn code: 1"
        assert str(error) == expected_message
        assert error.command == "ls -la"
        assert error.return_code == 1

    def test_process_error_with_command_list(self) -> None:
        """Test ProcessError with list command."""
        error = ProcessError(
            "Command failed",
            command=["ls", "-la", "/nonexistent"],
            return_code=2,
        )

        expected_message = "Command failed\nCommand: ls -la /nonexistent\nReturn code: 2"
        assert str(error) == expected_message
        assert error.command == ["ls", "-la", "/nonexistent"]
        assert error.return_code == 2

    def test_process_error_with_timeout(self) -> None:
        """Test ProcessError with timeout flag."""
        error = ProcessError("Process timed out", command="sleep 10", timeout=True)

        expected_message = "Process timed out\nCommand: sleep 10\nProcess timed out"
        assert str(error) == expected_message
        assert error.timeout is True

    def test_process_error_with_stdout_string(self) -> None:
        """Test ProcessError with string stdout."""
        error = ProcessError(
            "Command output",
            command="echo hello",
            stdout="hello world\n",
        )

        expected_message = "Command output\nCommand: echo hello\n--- STDOUT ---\nhello world"
        assert str(error) == expected_message
        assert error.stdout == "hello world"

    def test_process_error_with_stdout_bytes(self) -> None:
        """Test ProcessError with bytes stdout."""
        error = ProcessError(
            "Command output",
            command="cat file.txt",
            stdout=b"binary content\n",
        )

        expected_message = "Command output\nCommand: cat file.txt\n--- STDOUT ---\nbinary content"
        assert str(error) == expected_message
        assert error.stdout == "binary content"

    def test_process_error_with_stderr_string(self) -> None:
        """Test ProcessError with string stderr."""
        error = ProcessError(
            "Command failed",
            command="cat /nonexistent",
            stderr="cat: /nonexistent: No such file or directory\n",
        )

        expected_message = "Command failed\nCommand: cat /nonexistent\n--- STDERR ---\ncat: /nonexistent: No such file or directory"
        assert str(error) == expected_message
        assert error.stderr == "cat: /nonexistent: No such file or directory"

    def test_process_error_with_stderr_bytes(self) -> None:
        """Test ProcessError with bytes stderr."""
        error = ProcessError(
            "Command failed",
            command="invalid_command",
            stderr=b"command not found\n",
        )

        expected_message = "Command failed\nCommand: invalid_command\n--- STDERR ---\ncommand not found"
        assert str(error) == expected_message
        assert error.stderr == "command not found"

    def test_process_error_with_both_outputs(self) -> None:
        """Test ProcessError with both stdout and stderr."""
        error = ProcessError(
            "Mixed output",
            command="test_cmd",
            stdout="successful part\n",
            stderr="warning message\n",
        )

        expected_message = (
            "Mixed output\nCommand: test_cmd\n--- STDOUT ---\nsuccessful part\n--- STDERR ---\nwarning message"
        )
        assert str(error) == expected_message
        assert error.stdout == "successful part"
        assert error.stderr == "warning message"

    def test_process_error_with_empty_stdout(self) -> None:
        """Test ProcessError with empty stdout (should be ignored)."""
        error = ProcessError("No output", command="silent_cmd", stdout="")

        expected_message = "No output\nCommand: silent_cmd"
        assert str(error) == expected_message
        assert error.stdout is None

    def test_process_error_with_empty_stderr(self) -> None:
        """Test ProcessError with empty stderr (should be ignored)."""
        error = ProcessError("No errors", command="clean_cmd", stderr="")

        expected_message = "No errors\nCommand: clean_cmd"
        assert str(error) == expected_message
        assert error.stderr is None

    def test_process_error_with_whitespace_only_stdout(self) -> None:
        """Test ProcessError with whitespace-only stdout (should be stripped to empty)."""
        error = ProcessError(
            "Whitespace output",
            command="space_cmd",
            stdout="   \n\t  \n   ",
        )

        expected_message = "Whitespace output\nCommand: space_cmd"
        assert str(error) == expected_message
        assert error.stdout == ""

    def test_process_error_with_whitespace_only_stderr(self) -> None:
        """Test ProcessError with whitespace-only stderr (should be stripped to empty)."""
        error = ProcessError(
            "Whitespace errors",
            command="space_cmd",
            stderr="   \n\t  \n   ",
        )

        expected_message = "Whitespace errors\nCommand: space_cmd"
        assert str(error) == expected_message
        assert error.stderr == ""

    def test_process_error_with_extra_context(self) -> None:
        """Test ProcessError with extra context information."""
        error = ProcessError(
            "Context test",
            command="test_cmd",
            return_code=42,
            custom_field="custom_value",
            another_field=123,
        )

        # Check that extra context is stored
        assert error.context["custom_field"] == "custom_value"
        assert error.context["another_field"] == 123
        assert error.context["process.command"] == "test_cmd"
        assert error.context["process.return_code"] == 42
        assert error.context["process.timeout"] is False

    def test_process_error_comprehensive_scenario(self) -> None:
        """Test ProcessError with all parameters."""
        error = ProcessError(
            "Full test",
            command=["complex", "command", "--flag"],
            return_code=127,
            stdout=b"output data\n",
            stderr=b"error data\n",
            timeout=True,
            env_var="TEST_ENV",
            working_dir="/tmp",
        )

        expected_message = (
            "Full test\nCommand: complex command --flag\n"
            "Return code: 127\nProcess timed out\n"
            "--- STDOUT ---\noutput data\n"
            "--- STDERR ---\nerror data"
        )
        assert str(error) == expected_message
        assert error.command == ["complex", "command", "--flag"]
        assert error.return_code == 127
        assert error.stdout == "output data"
        assert error.stderr == "error data"
        assert error.timeout is True
        assert error.context["env_var"] == "TEST_ENV"
        assert error.context["working_dir"] == "/tmp"


class TestCommandNotFoundError(FoundationTestCase):
    """Test CommandNotFoundError class."""

    def test_command_not_found_basic(self) -> None:
        """Test basic CommandNotFoundError."""
        error = CommandNotFoundError("Command not found")

        assert str(error) == "Command not found"
        assert error._default_code() == "COMMAND_NOT_FOUND"
        assert isinstance(error, ProcessError)

    def test_command_not_found_with_command(self) -> None:
        """Test CommandNotFoundError with command details."""
        error = CommandNotFoundError(
            "Command not found",
            command="nonexistent_command",
            return_code=127,
        )

        expected_message = "Command not found\nCommand: nonexistent_command\nReturn code: 127"
        assert str(error) == expected_message
        assert error.command == "nonexistent_command"
        assert error.return_code == 127
        assert error._default_code() == "COMMAND_NOT_FOUND"

    def test_command_not_found_with_stderr(self) -> None:
        """Test CommandNotFoundError with stderr output."""
        error = CommandNotFoundError(
            "Command not available",
            command="missing_tool",
            stderr="bash: missing_tool: command not found",
        )

        expected_message = (
            "Command not available\nCommand: missing_tool\n"
            "--- STDERR ---\nbash: missing_tool: command not found"
        )
        assert str(error) == expected_message
        assert error.stderr == "bash: missing_tool: command not found"


class TestProcessTimeoutError(FoundationTestCase):
    """Test ProcessTimeoutError class."""

    def test_process_timeout_basic(self) -> None:
        """Test basic ProcessTimeoutError."""
        error = ProcessTimeoutError("Process timed out")

        assert str(error) == "Process timed out\nProcess timed out"
        assert error._default_code() == "PROCESS_TIMEOUT"
        assert error.timeout is True
        assert isinstance(error, ProcessError)

    def test_process_timeout_with_command(self) -> None:
        """Test ProcessTimeoutError with command."""
        error = ProcessTimeoutError(
            "Timeout occurred",
            command="long_running_cmd",
            timeout_seconds=30.0,
        )

        expected_message = "Timeout occurred\nCommand: long_running_cmd\nProcess timed out"
        assert str(error) == expected_message
        assert error.command == "long_running_cmd"
        assert error.timeout is True
        assert error.context["process.timeout_seconds"] == 30.0

    def test_process_timeout_with_outputs(self) -> None:
        """Test ProcessTimeoutError with partial outputs."""
        error = ProcessTimeoutError(
            "Timeout with output",
            command=["slow_process", "--verbose"],
            timeout_seconds=60.0,
            stdout="Partial output before timeout\n",
            stderr="Warning: slow operation\n",
        )

        expected_message = (
            "Timeout with output\nCommand: slow_process --verbose\n"
            "Process timed out\n--- STDOUT ---\nPartial output before timeout\n"
            "--- STDERR ---\nWarning: slow operation"
        )
        assert str(error) == expected_message
        assert error.stdout == "Partial output before timeout"
        assert error.stderr == "Warning: slow operation"
        assert error.context["process.timeout_seconds"] == 60.0
        assert error.timeout is True

    def test_process_timeout_with_bytes_outputs(self) -> None:
        """Test ProcessTimeoutError with bytes outputs."""
        error = ProcessTimeoutError(
            "Timeout with bytes",
            command="binary_process",
            timeout_seconds=45.0,
            stdout=b"binary stdout\n",
            stderr=b"binary stderr\n",
        )

        expected_message = (
            "Timeout with bytes\nCommand: binary_process\n"
            "Process timed out\n--- STDOUT ---\nbinary stdout\n"
            "--- STDERR ---\nbinary stderr"
        )
        assert str(error) == expected_message
        assert error.stdout == "binary stdout"
        assert error.stderr == "binary stderr"

    def test_process_timeout_with_extra_context(self) -> None:
        """Test ProcessTimeoutError with additional context."""
        error = ProcessTimeoutError(
            "Context timeout",
            command="context_cmd",
            timeout_seconds=120.0,
            process_id=12345,
            signal_used="SIGTERM",
        )

        assert error.context["process.timeout_seconds"] == 120.0
        assert error.context["process_id"] == 12345
        assert error.context["signal_used"] == "SIGTERM"
        assert error.timeout is True


class TestProcessErrorInheritance(FoundationTestCase):
    """Test inheritance and polymorphism of process errors."""

    def test_all_are_process_errors(self) -> None:
        """Test that all error types inherit from ProcessError."""
        process_error = ProcessError("base error")
        command_error = CommandNotFoundError("command error")
        timeout_error = ProcessTimeoutError("timeout error")

        assert isinstance(command_error, ProcessError)
        assert isinstance(timeout_error, ProcessError)
        assert all(hasattr(error, "_default_code") for error in [process_error, command_error, timeout_error])

    def test_unique_error_codes(self) -> None:
        """Test that each error type has unique error code."""
        process_error = ProcessError("base")
        command_error = CommandNotFoundError("command")
        timeout_error = ProcessTimeoutError("timeout")

        codes = {
            process_error._default_code(),
            command_error._default_code(),
            timeout_error._default_code(),
        }

        assert len(codes) == 3  # All unique
        assert "PROCESS_ERROR" in codes
        assert "COMMAND_NOT_FOUND" in codes
        assert "PROCESS_TIMEOUT" in codes

    def test_polymorphic_behavior(self) -> None:
        """Test polymorphic behavior of process error types."""
        errors = [
            ProcessError("base error", return_code=1),
            CommandNotFoundError("not found", command="missing"),
            ProcessTimeoutError("timeout", timeout_seconds=30.0),
        ]

        # All should have common attributes
        for error in errors:
            assert hasattr(error, "command")
            assert hasattr(error, "return_code")
            assert hasattr(error, "stdout")
            assert hasattr(error, "stderr")
            assert hasattr(error, "timeout")
            assert callable(error._default_code)

        # Timeout error should always have timeout=True
        assert not errors[0].timeout  # ProcessError
        assert not errors[1].timeout  # CommandNotFoundError
        assert errors[2].timeout  # ProcessTimeoutError


# 🧱🏗️🔚
