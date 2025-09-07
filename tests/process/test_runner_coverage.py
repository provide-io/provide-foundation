#
# test_runner_coverage.py
#
"""
Additional tests to achieve full coverage for process/runner.py.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from provide.foundation.process.runner import (
    ProcessError,
    TimeoutError, 
    run_command,
    run_shell,
    stream_command,
)


class TestInputHandling:
    """Test input handling and conversion for different text modes."""
    
    def test_bytes_input_with_text_mode(self):
        """Test bytes input gets converted to string in text mode."""
        # Use echo command that reads from stdin
        result = run_command(
            ["cat"], 
            input=b"hello world",
            text=True,
            capture_output=True
        )
        
        assert result.returncode == 0
        assert "hello world" in result.stdout
    
    def test_string_input_with_binary_mode(self):
        """Test string input gets converted to bytes in binary mode."""
        result = run_command(
            ["cat"],
            input="hello world", 
            text=False,
            capture_output=True
        )
        
        assert result.returncode == 0
        assert b"hello world" in result.stdout
    
    def test_matching_input_types(self):
        """Test that matching input types are passed through unchanged."""
        # String input with text mode - should pass through
        result = run_command(
            ["cat"],
            input="hello world",
            text=True, 
            capture_output=True
        )
        
        assert result.returncode == 0
        assert "hello world" in result.stdout
        
        # Bytes input with binary mode - should pass through  
        result = run_command(
            ["cat"],
            input=b"hello world",
            text=False,
            capture_output=True
        )
        
        assert result.returncode == 0
        assert b"hello world" in result.stdout
    
    def test_none_input(self):
        """Test that None input is handled correctly."""
        result = run_command(["echo", "test"], input=None)
        assert result.returncode == 0


class TestErrorHandling:
    """Test error handling paths in runner."""
    
    def test_subprocess_timeout_error(self):
        """Test handling of subprocess TimeoutExpired error."""
        with pytest.raises(TimeoutError) as exc_info:
            run_command(["sleep", "10"], timeout=0.01, check=True)
        
        assert "timed out" in str(exc_info.value).lower()
    
    @patch('subprocess.run')
    def test_generic_subprocess_exception(self, mock_run):
        """Test handling of generic subprocess exceptions."""
        # Mock subprocess.run to raise a generic exception
        mock_run.side_effect = OSError("File not found")
        
        with pytest.raises(ProcessError) as exc_info:
            run_command(["nonexistent_command"], check=True)
        
        assert "Failed to execute command" in str(exc_info.value)
        assert exc_info.value.code == "PROCESS_EXECUTION_FAILED"
    
    @patch('subprocess.run')
    def test_reraise_process_error(self, mock_run):
        """Test that ProcessError and TimeoutError are re-raised directly."""
        # Mock subprocess.run to raise a ProcessError
        original_error = ProcessError("Original error", command="test_command")
        mock_run.side_effect = original_error
        
        with pytest.raises(ProcessError) as exc_info:
            run_command(["test"], check=True)
        
        # Should be the same exception instance
        assert exc_info.value is original_error
    
    def test_command_failure_with_check_false(self):
        """Test that failed commands don't raise when check=False."""
        result = run_command(["false"], check=False)
        assert result.returncode != 0
        # Should not raise an exception
    
    def test_command_failure_with_check_true(self):
        """Test that failed commands raise ProcessError when check=True."""
        with pytest.raises(ProcessError) as exc_info:
            run_command(["false"], check=True)
        
        assert exc_info.value.returncode != 0
        assert exc_info.value.code == "PROCESS_COMMAND_FAILED"


class TestShellExecution:
    """Test shell execution paths."""
    
    def test_shell_with_complex_command(self):
        """Test shell execution with complex commands."""
        result = run_shell("echo 'hello world' | grep hello")
        
        assert result.returncode == 0
        assert "hello" in result.stdout
    
    def test_shell_with_environment_variables(self):
        """Test shell execution with custom environment."""
        result = run_shell(
            "echo $TEST_VAR",
            env={"TEST_VAR": "test_value"}
        )
        
        assert result.returncode == 0
        assert "test_value" in result.stdout
    
    def test_shell_failure(self):
        """Test shell command failure."""
        with pytest.raises(ProcessError):
            run_shell("exit 1", check=True)


class TestWorkingDirectory:
    """Test working directory handling."""
    
    def test_cwd_as_string(self, tmp_path):
        """Test working directory as string path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = run_command(
            ["cat", "test.txt"],
            cwd=str(tmp_path)
        )
        
        assert result.returncode == 0
        assert "test content" in result.stdout
    
    def test_cwd_as_path_object(self, tmp_path):
        """Test working directory as Path object."""
        test_file = tmp_path / "test.txt" 
        test_file.write_text("test content")
        
        result = run_command(
            ["cat", "test.txt"],
            cwd=tmp_path
        )
        
        assert result.returncode == 0
        assert "test content" in result.stdout


class TestEnvironmentHandling:
    """Test environment variable handling."""
    
    def test_env_dict_conversion(self):
        """Test that env dict is properly converted."""
        result = run_command(
            ["env"],
            env={"TEST_VAR": "test_value"},
            capture_output=True
        )
        
        assert result.returncode == 0
        assert "TEST_VAR=test_value" in result.stdout
    
    def test_env_none(self):
        """Test that None env is handled correctly."""
        result = run_command(["echo", "test"], env=None)
        assert result.returncode == 0
        # Should not crash or fail


class TestStreamCommandCoverage:
    """Test additional stream command functionality."""
    
    def test_stream_command_with_stderr(self):
        """Test streaming command with stderr capture."""
        lines = list(stream_command(
            [sys.executable, "-c", "import sys; print('stdout'); sys.stderr.write('stderr\\n')"],
            stream_stderr=True
        ))
        
        # Should capture both stdout and stderr
        assert len(lines) >= 1
        output = "".join(lines)
        assert "stdout" in output or "stderr" in output
    
    def test_stream_command_timeout(self):
        """Test stream command timeout handling."""
        with pytest.raises(TimeoutError):
            # Try to stream from a long-running command with short timeout
            list(stream_command(["sleep", "5"], timeout=0.1))
    
    @patch('subprocess.Popen')
    def test_stream_generic_exception(self, mock_popen):
        """Test stream command with generic exception."""
        mock_popen.side_effect = OSError("Command not found")
        
        with pytest.raises(ProcessError) as exc_info:
            list(stream_command(["nonexistent"]))
        
        assert "Failed to stream command" in str(exc_info.value)


class TestCompletedProcessConstruction:
    """Test CompletedProcess object construction."""
    
    def test_completed_process_with_list_cmd(self):
        """Test CompletedProcess construction with list command."""
        result = run_command(["echo", "hello"], capture_output=True)
        
        assert isinstance(result.args, list)
        assert result.args == ["echo", "hello"]
    
    def test_completed_process_with_string_cmd(self):
        """Test CompletedProcess construction with string command."""
        result = run_shell("echo hello", capture_output=True)
        
        assert isinstance(result.args, list)
        assert len(result.args) == 1  # String command becomes single-item list
        assert "echo hello" in result.args[0]
    
    def test_completed_process_without_capture(self):
        """Test CompletedProcess when capture_output=False."""
        result = run_command(["echo", "hello"], capture_output=False)
        
        # stdout/stderr should be empty strings when not captured
        assert result.stdout == ""
        assert result.stderr == ""
    
    def test_completed_process_env_handling(self):
        """Test CompletedProcess environment handling."""
        # Test with custom env
        result = run_command(
            ["echo", "test"], 
            env={"TEST_VAR": "value"},
            capture_output=True
        )
        assert result.env is not None
        assert "TEST_VAR" in result.env
        
        # Test with no env
        result = run_command(["echo", "test"], env=None, capture_output=True)
        assert result.env is None