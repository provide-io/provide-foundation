#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import subprocess
from typing import Any

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import (
    CompletedProcess,
    normalize_cwd,
    prepare_environment,
    prepare_input,
    validate_command_type,
)

"""Core sync subprocess execution."""

log = get_logger(__name__)


def run(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    text: bool = True,
    input: str | bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command with consistent error handling and logging.

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
        ProcessTimeoutError: If timeout is exceeded

    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    validate_command_type(cmd, shell)

    # Prepare environment
    run_env = prepare_environment(env)

    # Normalize cwd
    cwd = normalize_cwd(cwd)

    # Prepare input
    subprocess_input = prepare_input(input, text)

    try:
        # Prepare command for subprocess
        subprocess_cmd = cmd_str if shell else cmd

        result = subprocess.run(
            subprocess_cmd,
            cwd=cwd,
            env=run_env,
            capture_output=capture_output,
            text=text,
            input=subprocess_input,
            timeout=timeout,
            check=False,  # We'll handle the check ourselves
            shell=shell,  # nosec B602 - Shell usage validated by caller context
            **kwargs,
        )

        completed = CompletedProcess(
            args=cmd if isinstance(cmd, list) else [cmd],
            returncode=result.returncode,
            stdout=result.stdout if capture_output else "",
            stderr=result.stderr if capture_output else "",
            cwd=cwd,
            env=dict(env) if env else None,  # Only store caller overrides, not full run_env
        )

        if check and result.returncode != 0:
            log.error(
                "❌ Command failed",
                command=cmd_str,
                returncode=result.returncode,
                stderr=result.stderr if capture_output else None,
            )
            raise ProcessError(
                f"Command failed with exit code {result.returncode}: {cmd_str}",
                code="PROCESS_COMMAND_FAILED",
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ Command timed out",
            command=cmd_str,
            timeout=timeout,
        )
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e
    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error(
            "💥 Command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def run_simple(
    cmd: list[str],
    cwd: str | Path | None = None,
    **kwargs: Any,
) -> str:
    """Simple wrapper for run that returns stdout as a string.

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


# 🧱🏗️🔚
