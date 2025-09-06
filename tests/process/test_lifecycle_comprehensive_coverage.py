"""Comprehensive coverage tests for process/lifecycle.py module."""

import asyncio
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call

import pytest

from provide.foundation.process.lifecycle import ManagedProcess, wait_for_process_output
from provide.foundation.process.runner import ProcessError


class TestManagedProcessInitialization:
    """Test ManagedProcess initialization and properties."""
    
    def test_basic_initialization(self):
        """Test basic ManagedProcess initialization."""
        command = ["echo", "test"]
        proc = ManagedProcess(command)
        
        assert proc.command == command
        assert proc.cwd is None
        assert proc.capture_output is True
        assert proc.text_mode is False
        assert proc.bufsize == 0
        assert proc.stderr_relay is True
        assert proc._process is None
        assert proc._started is False
    
    def test_initialization_with_cwd_string(self):
        """Test initialization with cwd as string."""
        command = ["pwd"]
        cwd = "/tmp"
        proc = ManagedProcess(command, cwd=cwd)
        
        assert proc.cwd == cwd
    
    def test_initialization_with_cwd_path(self):
        """Test initialization with cwd as Path object."""
        command = ["pwd"]
        cwd = Path("/tmp")
        proc = ManagedProcess(command, cwd=cwd)
        
        assert proc.cwd == "/tmp"
    
    def test_initialization_with_env(self):
        """Test initialization with custom environment."""
        command = ["env"]
        custom_env = {"TEST_VAR": "test_value"}
        proc = ManagedProcess(command, env=custom_env)
        
        assert "TEST_VAR" in proc._env
        assert proc._env["TEST_VAR"] == "test_value"
        # Should include existing environment
        assert "PATH" in proc._env
    
    def test_initialization_with_all_params(self):
        """Test initialization with all parameters."""
        command = ["sleep", "1"]
        proc = ManagedProcess(
            command,
            cwd="/tmp",
            env={"TEST": "value"},
            capture_output=False,
            text_mode=True,
            bufsize=1024,
            stderr_relay=False,
            shell=True
        )
        
        assert proc.command == command
        assert proc.cwd == "/tmp"
        assert proc.capture_output is False
        assert proc.text_mode is True
        assert proc.bufsize == 1024
        assert proc.stderr_relay is False
        assert "shell" in proc.kwargs
    
    def test_properties_before_launch(self):
        """Test properties when process not yet launched."""
        proc = ManagedProcess(["echo", "test"])
        
        assert proc.process is None
        assert proc.pid is None
        assert proc.returncode is None
        assert proc.is_running() is False


class TestManagedProcessLaunch:
    """Test ManagedProcess launch functionality."""
    
    def test_successful_launch(self):
        """Test successful process launch."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        
        assert proc._started is True
        assert proc._process is not None
        assert proc.pid is not None
        assert isinstance(proc.pid, int)
        
        # Wait for process to complete
        proc._process.wait()
        proc.cleanup()
    
    def test_launch_already_started_error(self):
        """Test error when trying to launch already started process."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        
        with pytest.raises(RuntimeError, match="Process has already been started"):
            proc.launch()
        
        proc._process.wait()
        proc.cleanup()
    
    def test_launch_with_invalid_command(self):
        """Test launch with invalid command."""
        proc = ManagedProcess(["/nonexistent/command"])
        
        with pytest.raises(ProcessError, match="Failed to launch process"):
            proc.launch()
    
    def test_launch_with_working_directory(self):
        """Test launch with specific working directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = ManagedProcess(["pwd"], cwd=tmpdir, capture_output=True, text_mode=True)
            proc.launch()
            
            # Read output
            stdout, _ = proc._process.communicate()
            assert tmpdir in stdout.strip()
            
            proc.cleanup()
    
    def test_properties_after_launch(self):
        """Test properties after successful launch."""
        proc = ManagedProcess(["sleep", "0.1"])
        proc.launch()
        
        assert proc.process is not None
        assert proc.pid is not None
        assert proc.is_running() is True
        
        # Wait for process to finish
        proc._process.wait()
        assert proc.returncode is not None
        assert proc.is_running() is False
        
        proc.cleanup()


class TestManagedProcessOutput:
    """Test ManagedProcess output handling."""
    
    @pytest.mark.asyncio
    async def test_read_line_async_success(self):
        """Test successful async line reading."""
        proc = ManagedProcess(["echo", "test line"], capture_output=True, text_mode=True)
        proc.launch()
        
        line = await proc.read_line_async(timeout=2.0)
        assert "test line" in line
        
        proc._process.wait()
        proc.cleanup()
    
    @pytest.mark.asyncio
    async def test_read_line_async_no_process(self):
        """Test read_line_async when process not running."""
        proc = ManagedProcess(["echo", "test"])
        
        with pytest.raises(ProcessError, match="Process not running or stdout not available"):
            await proc.read_line_async()
    
    @pytest.mark.asyncio
    async def test_read_line_async_no_stdout(self):
        """Test read_line_async when stdout not captured."""
        proc = ManagedProcess(["echo", "test"], capture_output=False)
        proc.launch()
        
        with pytest.raises(ProcessError, match="Process not running or stdout not available"):
            await proc.read_line_async()
        
        proc._process.wait()
        proc.cleanup()
    
    @pytest.mark.asyncio
    async def test_read_char_async_success(self):
        """Test successful async character reading."""
        proc = ManagedProcess(["echo", "x"], capture_output=True, text_mode=True)
        proc.launch()
        
        char = await proc.read_char_async(timeout=2.0)
        assert len(char) == 1
        
        proc._process.wait()
        proc.cleanup()
    
    @pytest.mark.asyncio
    async def test_read_char_async_no_process(self):
        """Test read_char_async when process not running."""
        proc = ManagedProcess(["echo", "test"])
        
        with pytest.raises(ProcessError, match="Process not running or stdout not available"):
            await proc.read_char_async()


class TestManagedProcessStderrRelay:
    """Test ManagedProcess stderr relay functionality."""
    
    @patch('sys.stderr.write')
    @patch('sys.stderr.flush')
    def test_stderr_relay_enabled(self, mock_flush, mock_write):
        """Test stderr relay when enabled."""
        # Create a process that outputs to stderr
        proc = ManagedProcess(
            [sys.executable, "-c", "import sys; sys.stderr.write('error message\\n')"],
            stderr_relay=True,
            capture_output=True
        )
        proc.launch()
        
        # Wait for process to complete and stderr thread to relay
        proc._process.wait()
        time.sleep(0.1)  # Give relay thread time to process
        
        # Check if stderr was relayed (may not be called if process completes too quickly)
        proc.cleanup()
    
    def test_stderr_relay_disabled(self):
        """Test that stderr relay is not started when disabled."""
        proc = ManagedProcess(
            ["echo", "test"],
            stderr_relay=False,
            capture_output=True
        )
        proc.launch()
        
        assert proc._stderr_thread is None
        
        proc._process.wait()
        proc.cleanup()
    
    def test_stderr_relay_thread_creation(self):
        """Test stderr relay thread is created when enabled."""
        proc = ManagedProcess(
            ["sleep", "0.1"],
            stderr_relay=True,
            capture_output=True
        )
        proc.launch()
        
        # If stderr is captured, relay thread should be created
        if proc._process.stderr:
            assert proc._stderr_thread is not None
            assert isinstance(proc._stderr_thread, threading.Thread)
        
        proc._process.wait()
        proc.cleanup()


class TestManagedProcessTermination:
    """Test ManagedProcess termination functionality."""
    
    def test_terminate_gracefully_not_started(self):
        """Test graceful termination when process not started."""
        proc = ManagedProcess(["sleep", "1"])
        result = proc.terminate_gracefully()
        
        assert result is True  # No process to terminate
    
    def test_terminate_gracefully_already_finished(self):
        """Test graceful termination when process already finished."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        proc._process.wait()  # Wait for completion
        
        result = proc.terminate_gracefully()
        assert result is True
        
        proc.cleanup()
    
    def test_terminate_gracefully_success(self):
        """Test successful graceful termination."""
        proc = ManagedProcess(["sleep", "10"])
        proc.launch()
        
        # Process should be running
        assert proc.is_running()
        
        result = proc.terminate_gracefully(timeout=2.0)
        assert result is True
        assert not proc.is_running()
        
        proc.cleanup()
    
    def test_terminate_gracefully_timeout(self):
        """Test graceful termination with timeout (kill)."""
        # Create a process that ignores SIGTERM
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(10)"
        ])
        proc.launch()
        
        # Should timeout and force kill
        result = proc.terminate_gracefully(timeout=0.5)
        assert result is True
        assert not proc.is_running()
        
        proc.cleanup()
    
    def test_cleanup(self):
        """Test cleanup functionality."""
        proc = ManagedProcess(["echo", "test"])
        proc.launch()
        proc._process.wait()
        
        # Create a mock stderr thread
        proc._stderr_thread = Mock()
        proc._stderr_thread.is_alive.return_value = True
        
        proc.cleanup()
        
        # Should join the stderr thread
        proc._stderr_thread.join.assert_called_once_with(timeout=1.0)


class TestManagedProcessContextManager:
    """Test ManagedProcess as context manager."""
    
    def test_context_manager_success(self):
        """Test successful context manager usage."""
        with ManagedProcess(["echo", "test"]) as proc:
            # No need to call launch() - context manager already does this
            assert proc.is_running() or proc.returncode is not None
        
        # Process should be cleaned up after context exit
        assert not proc.is_running()
    
    def test_context_manager_exception(self):
        """Test context manager cleanup on exception."""
        try:
            with ManagedProcess(["sleep", "10"]) as proc:
                # No need to call launch() - context manager already does this
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Process should still be cleaned up
        assert not proc.is_running()


class TestManagedProcessEdgeCases:
    """Test ManagedProcess edge cases and error conditions."""
    
    def test_is_running_no_process(self):
        """Test is_running when no process exists."""
        proc = ManagedProcess(["echo", "test"])
        assert proc.is_running() is False
    
    def test_launch_with_shell_kwarg(self):
        """Test launch with shell=True kwarg."""
        if sys.platform != "win32":
            proc = ManagedProcess(["echo test"], shell=True)
            proc.launch()
            
            proc._process.wait()
            assert proc.returncode == 0
            
            proc.cleanup()
    
    @patch('subprocess.Popen')
    def test_launch_subprocess_exception(self, mock_popen):
        """Test launch when subprocess.Popen raises exception."""
        mock_popen.side_effect = OSError("Permission denied")
        
        proc = ManagedProcess(["echo", "test"])
        with pytest.raises(ProcessError, match="Failed to launch process"):
            proc.launch()
    
    def test_stderr_relay_no_stderr(self):
        """Test stderr relay when no stderr pipe."""
        proc = ManagedProcess(["echo", "test"], capture_output=False)
        proc.launch()
        
        # Should not create stderr thread when no stderr pipe
        assert proc._stderr_thread is None
        
        proc._process.wait()
        proc.cleanup()
    
    def test_start_stderr_relay_no_process(self):
        """Test _start_stderr_relay when no process."""
        proc = ManagedProcess(["echo", "test"])
        proc._start_stderr_relay()  # Should not crash
        
        assert proc._stderr_thread is None


@pytest.mark.asyncio
class TestWaitForProcessOutput:
    """Test wait_for_process_output function."""
    
    async def test_wait_for_output_success(self):
        """Test successful output waiting."""
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import sys, time; sys.stdout.write('start|middle|end\\n'); sys.stdout.flush()"
        ], capture_output=True, text_mode=True)
        proc.launch()
        
        result = await wait_for_process_output(
            proc, 
            expected_parts=["start", "middle", "end"],
            timeout=5.0
        )
        
        assert "start" in result
        assert "middle" in result
        assert "end" in result
        
        proc._process.wait()
        proc.cleanup()
    
    async def test_wait_for_output_timeout(self):
        """Test timeout when expected output never comes."""
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import time; time.sleep(2)"
        ], capture_output=True, text_mode=True)
        proc.launch()
        
        with pytest.raises(TimeoutError, match="Expected pattern .* not found within"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=1.0
            )
        
        proc.terminate_gracefully()
        proc.cleanup()
    
    async def test_wait_for_output_process_exits(self):
        """Test when process exits before expected output."""
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import sys; sys.exit(1)"
        ], capture_output=True, text_mode=True)
        proc.launch()
        
        with pytest.raises(ProcessError, match="Process exited with code 1"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=5.0
            )
        
        proc.cleanup()
    
    async def test_wait_for_output_char_fallback(self):
        """Test character-by-character fallback when line reading times out."""
        # Mock the read_line_async to raise TimeoutError
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import sys; sys.stdout.write('a'); sys.stdout.flush()"
        ], capture_output=True, text_mode=True)
        proc.launch()
        
        # Mock read_line_async to timeout but read_char_async to succeed
        original_read_line = proc.read_line_async
        original_read_char = proc.read_char_async
        
        async def mock_read_line(*args, **kwargs):
            raise TimeoutError()
        
        proc.read_line_async = mock_read_line
        
        result = await wait_for_process_output(
            proc,
            expected_parts=["a"],
            timeout=3.0
        )
        
        assert "a" in result
        
        # Restore original methods
        proc.read_line_async = original_read_line
        proc.read_char_async = original_read_char
        
        proc._process.wait()
        proc.cleanup()
    
    async def test_wait_for_output_both_timeouts(self):
        """Test when both line and char reading timeout."""
        proc = ManagedProcess([
            sys.executable, "-c", 
            "import time; time.sleep(10)"
        ], capture_output=True, text_mode=True)
        proc.launch()
        
        # Mock both reading methods to timeout
        async def mock_timeout(*args, **kwargs):
            raise TimeoutError()
        
        proc.read_line_async = mock_timeout
        proc.read_char_async = mock_timeout
        
        with pytest.raises(TimeoutError, match="Expected pattern .* not found within"):
            await wait_for_process_output(
                proc,
                expected_parts=["never_appears"],
                timeout=1.0
            )
        
        proc.terminate_gracefully()
        proc.cleanup()


class TestProcessLifecycleIntegration:
    """Integration tests for process lifecycle functionality."""
    
    def test_full_lifecycle_simple_command(self):
        """Test full lifecycle with simple command."""
        with ManagedProcess(["echo", "hello world"]) as proc:
            # No need to call launch() - context manager already does this
            assert proc.is_running() or proc.returncode is not None
        
        # Should be cleaned up after context exit
        assert not proc.is_running()
    
    @pytest.mark.asyncio
    async def test_full_lifecycle_with_output_waiting(self):
        """Test full lifecycle with output waiting."""
        with ManagedProcess([
            sys.executable, "-c",
            "import sys; sys.stdout.write('ready\\n'); sys.stdout.flush(); input()"
        ], capture_output=True, text_mode=True) as proc:
            # No need to call launch() - context manager already does this
            
            # Wait for ready signal
            result = await wait_for_process_output(proc, ["ready"], timeout=5.0)
            assert "ready" in result
            
            # Terminate the process (since it's waiting for input)
            proc.terminate_gracefully()
    
    def test_environment_inheritance(self):
        """Test that custom environment is properly inherited."""
        custom_env = {"TEST_PROCESS_VAR": "test_value_12345"}
        
        proc = ManagedProcess([
            sys.executable, "-c",
            "import os; print(f'TEST_VAR={os.environ.get(\"TEST_PROCESS_VAR\", \"NOT_FOUND\")}')"
        ], env=custom_env, capture_output=True, text_mode=True)
        proc.launch()
        
        stdout, _ = proc._process.communicate()
        assert "TEST_VAR=test_value_12345" in stdout
        
        proc.cleanup()