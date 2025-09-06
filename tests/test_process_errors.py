#
# tests/test_process_errors.py
#
"""Tests for provide.foundation.errors.process module."""

import pytest

from provide.foundation.errors.process import (
    CommandNotFoundError,
    ProcessError,
    ProcessTimeoutError,
)


class TestProcessError:
    """Test ProcessError functionality."""

    def test_basic_process_error(self) -> None:
        """Test creating a basic process error."""
        error = ProcessError("Command failed")
        
        assert str(error) == "Command failed"
        assert error.command is None
        assert error.return_code is None
        assert error.stdout is None
        assert error.stderr is None
        assert error.timeout is False
        assert error.code == "PROCESS_ERROR"

    def test_process_error_with_command(self) -> None:
        """Test process error with command information."""
        error = ProcessError(
            "Command execution failed",
            command=["ls", "-la", "/nonexistent"]
        )
        
        assert "Command: ls -la /nonexistent" in str(error)
        assert error.command == ["ls", "-la", "/nonexistent"]

    def test_process_error_with_command_string(self) -> None:
        """Test process error with command as string."""
        error = ProcessError(
            "Command execution failed",
            command="ls -la /nonexistent"
        )
        
        assert "Command: ls -la /nonexistent" in str(error)
        assert error.command == "ls -la /nonexistent"

    def test_process_error_with_return_code(self) -> None:
        """Test process error with return code."""
        error = ProcessError(
            "Command failed",
            command="ls /nonexistent",
            return_code=2
        )
        
        assert "Return code: 2" in str(error)
        assert error.return_code == 2

    def test_process_error_with_stdout_bytes(self) -> None:
        """Test process error with stdout as bytes."""
        stdout = b"Some output\nLine 2"
        error = ProcessError(
            "Command failed",
            stdout=stdout
        )
        
        assert "--- STDOUT ---" in str(error)
        assert "Some output\nLine 2" in str(error)
        assert error.stdout == "Some output\nLine 2"

    def test_process_error_with_stdout_string(self) -> None:
        """Test process error with stdout as string."""
        stdout = "String output\nAnother line"
        error = ProcessError(
            "Command failed",
            stdout=stdout
        )
        
        assert "--- STDOUT ---" in str(error)
        assert "String output\nAnother line" in str(error)
        assert error.stdout == "String output\nAnother line"

    def test_process_error_with_stderr_bytes(self) -> None:
        """Test process error with stderr as bytes."""
        stderr = b"Error message\nAnother error"
        error = ProcessError(
            "Command failed",
            stderr=stderr
        )
        
        assert "--- STDERR ---" in str(error)
        assert "Error message\nAnother error" in str(error)
        assert error.stderr == "Error message\nAnother error"

    def test_process_error_with_stderr_string(self) -> None:
        """Test process error with stderr as string."""
        stderr = "String error\nMore errors"
        error = ProcessError(
            "Command failed",
            stderr=stderr
        )
        
        assert "--- STDERR ---" in str(error)
        assert "String error\nMore errors" in str(error)
        assert error.stderr == "String error\nMore errors"

    def test_process_error_with_empty_outputs(self) -> None:
        """Test process error with empty stdout/stderr."""
        error = ProcessError(
            "Command failed",
            stdout="",
            stderr=""
        )
        
        # Empty outputs should not appear in message
        assert "--- STDOUT ---" not in str(error)
        assert "--- STDERR ---" not in str(error)
        assert error.stdout is None
        assert error.stderr is None

    def test_process_error_with_whitespace_outputs(self) -> None:
        """Test process error with whitespace-only outputs."""
        error = ProcessError(
            "Command failed",
            stdout="   \n  \t  ",
            stderr="\n\n   \n"
        )
        
        # Whitespace-only outputs should not appear
        assert "--- STDOUT ---" not in str(error)
        assert "--- STDERR ---" not in str(error)
        assert error.stdout is None
        assert error.stderr is None

    def test_process_error_with_timeout(self) -> None:
        """Test process error with timeout flag."""
        error = ProcessError(
            "Command timed out",
            timeout=True
        )
        
        assert "Process timed out" in str(error)
        assert error.timeout is True

    def test_process_error_complete(self) -> None:
        """Test process error with all parameters."""
        error = ProcessError(
            "Full command failure",
            command=["python", "script.py"],
            return_code=1,
            stdout="Output line 1\nOutput line 2",
            stderr="Error line 1\nError line 2",
            timeout=False,
            extra_context="test_value"
        )
        
        error_str = str(error)
        assert "Full command failure" in error_str
        assert "Command: python script.py" in error_str
        assert "Return code: 1" in error_str
        assert "--- STDOUT ---" in error_str
        assert "Output line 1\nOutput line 2" in error_str
        assert "--- STDERR ---" in error_str
        assert "Error line 1\nError line 2" in error_str
        
        # Check structured data
        assert error.command == ["python", "script.py"]
        assert error.return_code == 1
        assert error.stdout == "Output line 1\nOutput line 2"
        assert error.stderr == "Error line 1\nError line 2"
        assert error.timeout is False
        assert error.context["extra_context"] == "test_value"

    def test_process_error_context(self) -> None:
        """Test process error context data."""
        error = ProcessError(
            "Command failed",
            command="test_cmd",
            return_code=42,
            timeout=True
        )
        
        context = error.context
        assert context["process.command"] == "test_cmd"
        assert context["process.return_code"] == 42
        assert context["process.timeout"] is True

    def test_process_error_to_dict(self) -> None:
        """Test converting process error to dictionary."""
        error = ProcessError(
            "Command failed",
            command="test_cmd",
            return_code=1
        )
        
        error_dict = error.to_dict()
        assert error_dict["error.type"] == "ProcessError"
        assert error_dict["error.message"] == str(error)  # Full message with command info
        assert error_dict["error.code"] == "PROCESS_ERROR"
        assert error_dict["process.command"] == "test_cmd"
        assert error_dict["process.return_code"] == 1


class TestCommandNotFoundError:
    """Test CommandNotFoundError functionality."""

    def test_command_not_found_error(self) -> None:
        """Test CommandNotFoundError creation."""
        error = CommandNotFoundError(
            "Command not found",
            command="nonexistent_command"
        )
        
        assert error.code == "COMMAND_NOT_FOUND"
        assert "Command: nonexistent_command" in str(error)
        assert isinstance(error, ProcessError)


class TestProcessTimeoutError:
    """Test ProcessTimeoutError functionality."""

    def test_process_timeout_error(self) -> None:
        """Test ProcessTimeoutError creation."""
        error = ProcessTimeoutError(
            "Command timed out",
            command="slow_command",
            timeout_seconds=30.0
        )
        
        assert error.code == "PROCESS_TIMEOUT"
        assert error.timeout is True
        assert "Process timed out" in str(error)
        assert error.context["process.timeout_seconds"] == 30.0
        assert isinstance(error, ProcessError)

    def test_process_timeout_error_with_outputs(self) -> None:
        """Test ProcessTimeoutError with command outputs."""
        error = ProcessTimeoutError(
            "Long running command timed out",
            command=["long_running_script.sh"],
            timeout_seconds=60.0,
            stdout="Partial output before timeout",
            stderr="Warning messages"
        )
        
        assert "--- STDOUT ---" in str(error)
        assert "Partial output before timeout" in str(error)
        assert "--- STDERR ---" in str(error)
        assert "Warning messages" in str(error)
        assert error.timeout is True
        assert error.context["process.timeout_seconds"] == 60.0


# 🏗️🧪⚡️🪄