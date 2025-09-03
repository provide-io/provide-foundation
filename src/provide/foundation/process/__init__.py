"""Process execution utilities.

Unified subprocess execution with sync and async support.
"""

import asyncio
from collections.abc import AsyncIterator, Iterator, Mapping
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
from typing import Any

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

plog = get_logger(__name__)


class ProcessError(FoundationError):
    """Process execution error."""
    pass


class TimeoutError(ProcessError):
    """Process execution timed out."""
    pass


@dataclass
class CompletedProcess:
    """Result of a completed process."""
    
    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    cwd: str | None = None
    env: dict[str, str] | None = None


# ============================================================================
# Synchronous Execution
# ============================================================================

def run(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    text: bool = True,
    input: str | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """
    Run a subprocess command with consistent error handling and logging.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        text: Whether to decode output as text
        input: Input to send to the process
        shell: Whether to run command through shell
        **kwargs: Additional arguments passed to subprocess.run
    
    Returns:
        CompletedProcess with results
    
    Raises:
        ProcessError: If command fails and check=True
        TimeoutError: If timeout is exceeded
    """
    # Log command execution
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🚀 Running command", command=cmd_str, cwd=str(cwd) if cwd else None)
    
    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()
    
    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=run_env,
            capture_output=capture_output,
            text=text,
            input=input,
            timeout=timeout,
            check=False,  # We'll handle the check ourselves
            shell=shell,
            **kwargs,
        )
        
        completed = CompletedProcess(
            args=cmd if isinstance(cmd, list) else [cmd],
            returncode=result.returncode,
            stdout=result.stdout if capture_output else "",
            stderr=result.stderr if capture_output else "",
            cwd=cwd,
            env=dict(run_env) if env else None,
        )
        
        if check and result.returncode != 0:
            plog.error(
                "❌ Command failed",
                command=cmd_str,
                returncode=result.returncode,
                stderr=result.stderr if capture_output else None,
            )
            raise ProcessError(
                f"Command failed with exit code {result.returncode}: {cmd_str}",
                code="PROCESS_COMMAND_FAILED",
                command=cmd_str,
                returncode=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )
        
        plog.debug(
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )
        
        return completed
        
    except subprocess.TimeoutExpired as e:
        plog.error(
            "⏱️ Command timed out",
            command=cmd_str,
            timeout=timeout,
        )
        raise TimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_TIMEOUT",
            command=cmd_str,
            timeout=timeout,
        ) from e
    except Exception as e:
        if isinstance(e, (ProcessError, TimeoutError)):
            raise
        plog.error(
            "💥 Command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
            error=str(e),
        ) from e


def run_simple(
    cmd: list[str],
    cwd: str | Path | None = None,
    **kwargs: Any,
) -> str:
    """
    Simple wrapper for run that returns stdout as a string.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        **kwargs: Additional arguments passed to run
    
    Returns:
        Stdout as a stripped string
    
    Raises:
        ProcessError: If command fails
    """
    result = run(cmd, cwd=cwd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def stream(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> Iterator[str]:
    """
    Stream command output line by line.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        **kwargs: Additional arguments passed to subprocess.Popen
    
    Yields:
        Lines of output from the command
    
    Raises:
        ProcessError: If command fails
        TimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)
    
    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()
    
    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )
        
        if process.stdout:
            for line in process.stdout:
                yield line.rstrip()
        
        # Wait for process to complete
        returncode = process.wait(timeout=timeout)
        
        if returncode != 0:
            raise ProcessError(
                f"Command failed with exit code {returncode}: {cmd_str}",
                code="PROCESS_STREAM_FAILED",
                command=cmd_str,
                returncode=returncode,
            )
        
        plog.debug("✅ Stream completed", command=cmd_str)
        
    except subprocess.TimeoutExpired as e:
        process.kill()
        plog.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise TimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout=timeout,
        ) from e
    except Exception as e:
        if isinstance(e, (ProcessError, TimeoutError)):
            raise
        plog.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e


# ============================================================================
# Asynchronous Execution
# ============================================================================

async def async_run(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    **kwargs: Any,
) -> CompletedProcess:
    """
    Run a subprocess command asynchronously.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        **kwargs: Additional arguments
    
    Returns:
        CompletedProcess with results
    
    Raises:
        ProcessError: If command fails and check=True
        TimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🚀 Running async command", command=cmd_str, cwd=str(cwd) if cwd else None)
    
    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()
    
    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)
    
    try:
        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            env=run_env,
            stdout=asyncio.subprocess.PIPE if capture_output else None,
            stderr=asyncio.subprocess.PIPE if capture_output else None,
            stdin=asyncio.subprocess.PIPE if input else None,
            **kwargs,
        )
        
        # Communicate with process
        if timeout:
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=input),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                plog.error("⏱️ Async command timed out", command=cmd_str, timeout=timeout)
                raise TimeoutError(
                    f"Command timed out after {timeout}s: {cmd_str}",
                    code="PROCESS_ASYNC_TIMEOUT",
                    command=cmd_str,
                    timeout=timeout,
                )
        else:
            stdout, stderr = await process.communicate(input=input)
        
        # Decode output
        stdout_str = stdout.decode() if stdout else ""
        stderr_str = stderr.decode() if stderr else ""
        
        completed = CompletedProcess(
            args=cmd,
            returncode=process.returncode or 0,
            stdout=stdout_str,
            stderr=stderr_str,
            cwd=cwd,
            env=dict(run_env) if env else None,
        )
        
        if check and process.returncode != 0:
            plog.error(
                "❌ Async command failed",
                command=cmd_str,
                returncode=process.returncode,
                stderr=stderr_str if capture_output else None,
            )
            raise ProcessError(
                f"Command failed with exit code {process.returncode}: {cmd_str}",
                code="PROCESS_ASYNC_FAILED",
                command=cmd_str,
                returncode=process.returncode,
                stdout=stdout_str if capture_output else None,
                stderr=stderr_str if capture_output else None,
            )
        
        plog.debug(
            "✅ Async command completed",
            command=cmd_str,
            returncode=process.returncode,
        )
        
        return completed
        
    except Exception as e:
        if isinstance(e, (ProcessError, TimeoutError)):
            raise
        
        plog.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
            error=str(e),
        ) from e


async def async_stream(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """
    Stream command output line by line asynchronously.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        **kwargs: Additional arguments
    
    Yields:
        Lines of output from the command
    
    Raises:
        ProcessError: If command fails
        TimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)
    
    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()
    
    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)
    
    try:
        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            env=run_env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            **kwargs,
        )
        
        # Stream output with timeout
        start_time = asyncio.get_event_loop().time()
        
        if process.stdout:
            async for line in process.stdout:
                # Check timeout
                if timeout and (asyncio.get_event_loop().time() - start_time) > timeout:
                    process.kill()
                    await process.wait()
                    plog.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
                    raise TimeoutError(
                        f"Command timed out after {timeout}s: {cmd_str}",
                        code="PROCESS_ASYNC_STREAM_TIMEOUT",
                        command=cmd_str,
                        timeout=timeout,
                    )
                
                yield line.decode().rstrip()
        
        # Wait for process to complete
        await process.wait()
        
        if process.returncode != 0:
            raise ProcessError(
                f"Command failed with exit code {process.returncode}: {cmd_str}",
                code="PROCESS_ASYNC_STREAM_FAILED",
                command=cmd_str,
                returncode=process.returncode,
            )
        
        plog.debug("✅ Async stream completed", command=cmd_str)
        
    except Exception as e:
        if isinstance(e, (ProcessError, TimeoutError)):
            raise
        
        plog.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e


# ============================================================================
# Legacy Compatibility (deprecated names)
# ============================================================================

# Keep old names for backward compatibility (will be removed in v2.0)
run_command = run
run_command_simple = run_simple
stream_command = stream
async_run_command = async_run
async_stream_command = async_stream


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # New simplified names
    "run",
    "run_simple",
    "stream",
    "async_run",
    "async_stream",
    
    # Types
    "CompletedProcess",
    "ProcessError",
    "TimeoutError",
    
    # Legacy names (deprecated)
    "run_command",
    "run_command_simple",
    "stream_command",
    "async_run_command",
    "async_stream_command",
]