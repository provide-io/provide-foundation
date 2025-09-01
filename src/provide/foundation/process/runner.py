"""Core subprocess execution utilities."""

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
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


def run_command(
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


def run_command_simple(
    cmd: list[str],
    cwd: str | Path | None = None,
    **kwargs: Any,
) -> str:
    """
    Simple wrapper for run_command that returns stdout as a string.
    
    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        **kwargs: Additional arguments passed to run_command
    
    Returns:
        Stdout as a stripped string
    
    Raises:
        ProcessError: If command fails
    """
    result = run_command(cmd, cwd=cwd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def stream_command(
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
        plog.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e