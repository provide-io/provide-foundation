"""Tests for async process execution functionality."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock, call
from pathlib import Path

from provide.foundation.process import (
    async_run,
    async_stream,
    CompletedProcess,
    ProcessError,
    TimeoutError,
)


class TestAsyncRunCommand:
    """Test async_run function."""
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_success(self, mock_create):
        """Test successful async command execution."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b"output", b""))
        mock_create.return_value = mock_process
        
        result = await async_run(["echo", "hello"])
        
        assert isinstance(result, CompletedProcess)
        assert result.returncode == 0
        assert result.stdout == "output"
        assert result.stderr == ""
        assert result.args == ["echo", "hello"]
        
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args[0] == ("echo", "hello")
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_with_cwd(self, mock_create):
        """Test async command with working directory."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b"", b""))
        mock_create.return_value = mock_process
        
        result = await async_run(["ls"], cwd="/tmp")
        
        assert result.cwd == "/tmp"
        call_args = mock_create.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_with_path_cwd(self, mock_create):
        """Test async command with Path object as cwd."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b"", b""))
        mock_create.return_value = mock_process
        
        result = await async_run(["ls"], cwd=Path("/tmp"))
        
        assert result.cwd == "/tmp"
        call_args = mock_create.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_with_env(self, mock_create):
        """Test async command with custom environment."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b"", b""))
        mock_create.return_value = mock_process
        
        env = {"FOO": "bar", "PATH": "/usr/bin"}
        result = await async_run(["echo"], env=env)
        
        assert result.env == env
        call_args = mock_create.call_args
        assert call_args[1]["env"]["FOO"] == "bar"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_failure_with_check(self, mock_create):
        """Test async command failure raises ProcessError when check=True."""
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.communicate = AsyncMock(return_value=(b"", b"error message"))
        mock_create.return_value = mock_process
        
        with pytest.raises(ProcessError) as exc_info:
            await async_run(["false"], check=True)
        
        assert "exit code 1" in str(exc_info.value)
        assert exc_info.value.context["returncode"] == 1
        assert exc_info.value.context["stderr"] == "error message"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_failure_without_check(self, mock_create):
        """Test async command failure returns result when check=False."""
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.communicate = AsyncMock(return_value=(b"output", b"error"))
        mock_create.return_value = mock_process
        
        result = await async_run(["false"], check=False)
        
        assert result.returncode == 1
        assert result.stdout == "output"
        assert result.stderr == "error"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    @patch("asyncio.wait_for")
    async def test_async_run_timeout(self, mock_wait_for, mock_create):
        """Test async command timeout raises TimeoutError."""
        mock_process = MagicMock()
        mock_process.kill = MagicMock()
        mock_process.wait = AsyncMock()
        mock_create.return_value = mock_process
        mock_wait_for.side_effect = asyncio.TimeoutError()
        
        with pytest.raises(TimeoutError) as exc_info:
            await async_run(["sleep", "10"], timeout=1.0)
        
        assert "timed out after 1.0s" in str(exc_info.value)
        assert exc_info.value.context["timeout"] == 1.0
        mock_process.kill.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_with_input(self, mock_create):
        """Test async command with input."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(b"", b""))
        mock_create.return_value = mock_process
        
        await async_run(["cat"], input=b"test input")
        
        mock_process.communicate.assert_called_once_with(input=b"test input")
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_no_capture(self, mock_create):
        """Test async command without capturing output."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(None, None))
        mock_create.return_value = mock_process
        
        result = await async_run(["echo", "hello"], capture_output=False)
        
        assert result.stdout == ""
        assert result.stderr == ""
        call_args = mock_create.call_args
        assert call_args[1]["stdout"] is None
        assert call_args[1]["stderr"] is None
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_run_general_exception(self, mock_create):
        """Test async general exception handling."""
        mock_create.side_effect = Exception("Unexpected error")
        
        with pytest.raises(ProcessError) as exc_info:
            await async_run(["echo"])
        
        assert "Failed to execute async command" in str(exc_info.value)
        assert exc_info.value.context["error"] == "Unexpected error"


class TestAsyncStreamCommand:
    """Test async_stream function."""
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_stream_success(self, mock_create):
        """Test streaming async command output."""
        # Create mock stdout that yields lines
        class MockStdout:
            def __init__(self):
                self.lines = [b"line1\n", b"line2\n", b"line3\n"]
                self.index = 0
            
            def __aiter__(self):
                return self
            
            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line
        
        mock_process = MagicMock()
        mock_process.stdout = MockStdout()
        mock_process.returncode = 0
        mock_process.wait = AsyncMock()
        mock_create.return_value = mock_process
        
        lines = []
        async for line in async_stream(["cat", "file.txt"]):
            lines.append(line)
        
        assert lines == ["line1", "line2", "line3"]
        mock_process.wait.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_stream_with_cwd(self, mock_create):
        """Test async streaming with working directory."""
        class MockStdout:
            def __init__(self):
                self.lines = [b"output\n"]
                self.index = 0
            
            def __aiter__(self):
                return self
            
            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line
        
        mock_process = MagicMock()
        mock_process.stdout = MockStdout()
        mock_process.returncode = 0
        mock_process.wait = AsyncMock()
        mock_create.return_value = mock_process
        
        lines = []
        async for line in async_stream(["ls"], cwd="/tmp"):
            lines.append(line)
        
        call_args = mock_create.call_args
        assert call_args[1]["cwd"] == "/tmp"
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_stream_failure(self, mock_create):
        """Test async streaming command failure."""
        class MockStdout:
            def __init__(self):
                self.lines = [b"error line\n"]
                self.index = 0
            
            def __aiter__(self):
                return self
            
            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line
        
        mock_process = MagicMock()
        mock_process.stdout = MockStdout()
        mock_process.returncode = 1
        mock_process.wait = AsyncMock()
        mock_create.return_value = mock_process
        
        with pytest.raises(ProcessError) as exc_info:
            lines = []
            async for line in async_stream(["false"]):
                lines.append(line)
        
        assert "exit code 1" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    @patch("asyncio.get_event_loop")
    async def test_async_stream_timeout(self, mock_get_loop, mock_create):
        """Test async streaming command timeout."""
        # Mock event loop time
        mock_loop = MagicMock()
        mock_loop.time.side_effect = [0, 0.5, 1.5]  # Simulate time passing
        mock_get_loop.return_value = mock_loop
        
        class MockStdout:
            def __init__(self):
                self.lines = [b"line1\n", b"line2\n", b"line3\n"]
                self.index = 0
            
            def __aiter__(self):
                return self
            
            async def __anext__(self):
                if self.index >= len(self.lines):
                    raise StopAsyncIteration
                line = self.lines[self.index]
                self.index += 1
                return line
        
        mock_process = MagicMock()
        mock_process.stdout = MockStdout()
        mock_process.kill = MagicMock()
        mock_process.wait = AsyncMock()
        mock_create.return_value = mock_process
        
        with pytest.raises(TimeoutError) as exc_info:
            lines = []
            async for line in async_stream(["cat"], timeout=1.0):
                lines.append(line)
        
        assert "timed out after 1.0s" in str(exc_info.value)
        mock_process.kill.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("asyncio.create_subprocess_exec")
    async def test_async_stream_exception(self, mock_create):
        """Test async streaming command general exception."""
        mock_create.side_effect = Exception("Create failed")
        
        with pytest.raises(ProcessError) as exc_info:
            async for _ in async_stream(["echo"]):
                pass
        
        assert "Failed to stream async command" in str(exc_info.value)