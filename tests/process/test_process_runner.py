"""Tests for process execution functionality."""

import subprocess
import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path

from provide.foundation.process import (
    run,
    run_simple,
    stream,
    CompletedProcess,
    ProcessError,
    TimeoutError,
)


class TestRunCommand:
    """Test run_command function."""
    
    @patch("subprocess.run")
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="output",
            stderr="",
        )
        
        result = run(["echo", "hello"])
        
        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert result.stdout == "output"
        assert result.stderr == ""
        assert result.args == ["echo", "hello"]
        
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["echo", "hello"]
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True
    
    @patch("subprocess.run")
    def test_run_command_with_cwd(self, mock_run):
        """Test command execution with working directory."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        result = run(["ls"], cwd="/tmp")
        
        assert result.cwd == "/tmp"
        call_args = mock_run.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @patch("subprocess.run")
    def test_run_command_with_path_cwd(self, mock_run):
        """Test command execution with Path object as cwd."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        result = run(["ls"], cwd=Path("/tmp"))
        
        assert result.cwd == "/tmp"
        call_args = mock_run.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @patch("subprocess.run")
    def test_run_command_with_env(self, mock_run):
        """Test command execution with custom environment."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        env = {"FOO": "bar", "PATH": "/usr/bin"}
        result = run(["echo"], env=env)
        
        assert result.env == env
        call_args = mock_run.call_args
        assert call_args[1]["env"]["FOO"] == "bar"
    
    @patch("subprocess.run")
    def test_run_command_failure_with_check(self, mock_run):
        """Test command failure raises ProcessError when check=True."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error message",
        )
        
        with pytest.raises(ProcessError) as exc_info:
            run(["false"], check=True)
        
        assert "exit code 1" in str(exc_info.value)
        assert exc_info.value.context["returncode"] == 1
        assert exc_info.value.context["stderr"] == "error message"
    
    @patch("subprocess.run")
    def test_run_command_failure_without_check(self, mock_run):
        """Test command failure returns result when check=False."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="output",
            stderr="error",
        )
        
        result = run(["false"], check=False)
        
        assert result.returncode == 1
        assert result.stdout == "output"
        assert result.stderr == "error"
    
    @patch("subprocess.run")
    def test_run_command_timeout(self, mock_run):
        """Test command timeout raises TimeoutError."""
        mock_run.side_effect = subprocess.TimeoutExpired(["sleep", "10"], 1.0)
        
        with pytest.raises(TimeoutError) as exc_info:
            run(["sleep", "10"], timeout=1.0)
        
        assert "timed out after 1.0s" in str(exc_info.value)
        assert exc_info.value.context["timeout"] == 1.0
    
    @patch("subprocess.run")
    def test_run_command_with_input(self, mock_run):
        """Test command with input."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        run(["cat"], input="test input")
        
        call_args = mock_run.call_args
        assert call_args[1]["input"] == "test input"
    
    @patch("subprocess.run")
    def test_run_command_no_capture(self, mock_run):
        """Test command without capturing output."""
        mock_run.return_value = MagicMock(returncode=0)
        
        result = run(["echo", "hello"], capture_output=False)
        
        assert result.stdout == ""
        assert result.stderr == ""
        call_args = mock_run.call_args
        assert call_args[1]["capture_output"] is False
    
    @patch("subprocess.run")
    def test_run_command_shell(self, mock_run):
        """Test command with shell=True."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        run(["echo hello"], shell=True)
        
        call_args = mock_run.call_args
        assert call_args[1]["shell"] is True
    
    @patch("subprocess.run")
    def test_run_command_general_exception(self, mock_run):
        """Test general exception handling."""
        mock_run.side_effect = Exception("Unexpected error")
        
        with pytest.raises(ProcessError) as exc_info:
            run(["echo"])
        
        assert "Failed to execute command" in str(exc_info.value)
        assert exc_info.value.context["error"] == "Unexpected error"


class TestRunCommandSimple:
    """Test run_command_simple function."""
    
    @patch("subprocess.run")
    def test_run_command_simple_success(self, mock_run):
        """Test simple command returns stripped stdout."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="  output with spaces  \n",
            stderr="",
        )
        
        result = run_simple(["echo", "hello"])
        
        assert result == "output with spaces"
    
    @patch("subprocess.run")
    def test_run_command_simple_failure(self, mock_run):
        """Test simple command raises on failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error",
        )
        
        with pytest.raises(ProcessError):
            run_simple(["false"])


class TestStreamCommand:
    """Test stream_command function."""
    
    @patch("subprocess.Popen")
    def test_stream_command_success(self, mock_popen):
        """Test streaming command output."""
        mock_process = MagicMock()
        mock_process.stdout = ["line1\n", "line2\n", "line3\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        lines = list(stream(["cat", "file.txt"]))
        
        assert lines == ["line1", "line2", "line3"]
        mock_process.wait.assert_called_once()
    
    @patch("subprocess.Popen")
    def test_stream_command_with_cwd(self, mock_popen):
        """Test streaming with working directory."""
        mock_process = MagicMock()
        mock_process.stdout = ["output\n"]
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        list(stream(["ls"], cwd="/tmp"))
        
        call_args = mock_popen.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @patch("subprocess.Popen")
    def test_stream_command_failure(self, mock_popen):
        """Test streaming command failure."""
        mock_process = MagicMock()
        mock_process.stdout = ["error line\n"]
        mock_process.wait.return_value = 1
        mock_popen.return_value = mock_process
        
        with pytest.raises(ProcessError) as exc_info:
            list(stream(["false"]))
        
        assert "exit code 1" in str(exc_info.value)
    
    @patch("subprocess.Popen")
    def test_stream_command_timeout(self, mock_popen):
        """Test streaming command timeout."""
        mock_process = MagicMock()
        mock_process.stdout = ["line1\n"]
        mock_process.wait.side_effect = subprocess.TimeoutExpired(["cat"], 1.0)
        mock_process.kill = MagicMock()
        mock_popen.return_value = mock_process
        
        with pytest.raises(TimeoutError) as exc_info:
            list(stream(["cat"], timeout=1.0))
        
        assert "timed out after 1.0s" in str(exc_info.value)
        mock_process.kill.assert_called_once()
    
    @patch("subprocess.Popen")
    def test_stream_command_exception(self, mock_popen):
        """Test streaming command general exception."""
        mock_popen.side_effect = Exception("Popen failed")
        
        with pytest.raises(ProcessError) as exc_info:
            list(stream(["echo"]))
        
        assert "Failed to stream command" in str(exc_info.value)


class TestCompletedProcess:
    """Test CompletedProcess dataclass."""
    
    def test_completed_process_creation(self):
        """Test creating CompletedProcess instance."""
        proc = CompletedProcess(
            args=["echo", "hello"],
            returncode=0,
            stdout="hello",
            stderr="",
            cwd="/tmp",
            env={"FOO": "bar"},
        )
        
        assert proc.args == ["echo", "hello"]
        assert proc.returncode == 0
        assert proc.stdout == "hello"
        assert proc.stderr == ""
        assert proc.cwd == "/tmp"
        assert proc.env == {"FOO": "bar"}
    
    def test_completed_process_minimal(self):
        """Test creating CompletedProcess with minimal fields."""
        proc = CompletedProcess(
            args=["ls"],
            returncode=0,
            stdout="",
            stderr="",
        )
        
        assert proc.args == ["ls"]
        assert proc.returncode == 0
        assert proc.cwd is None
        assert proc.env is None