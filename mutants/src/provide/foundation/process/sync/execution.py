# provide/foundation/process/sync/execution.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_run__mutmut_orig(
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
            "✅ Command completed",
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


def x_run__mutmut_1(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = False,
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
            "✅ Command completed",
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


def x_run__mutmut_2(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = False,
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
            "✅ Command completed",
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


def x_run__mutmut_3(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    text: bool = False,
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
            "✅ Command completed",
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


def x_run__mutmut_4(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    text: bool = True,
    input: str | bytes | None = None,
    shell: bool = True,
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
            "✅ Command completed",
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


def x_run__mutmut_5(
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

    cmd_str = None
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
            "✅ Command completed",
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


def x_run__mutmut_6(
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

    cmd_str = " ".join(None) if isinstance(cmd, list) else str(cmd)
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
            "✅ Command completed",
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


def x_run__mutmut_7(
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

    cmd_str = "XX XX".join(cmd) if isinstance(cmd, list) else str(cmd)
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
            "✅ Command completed",
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


def x_run__mutmut_8(
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

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(None)
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
            "✅ Command completed",
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


def x_run__mutmut_9(
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
    masked_cmd = None
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
            "✅ Command completed",
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


def x_run__mutmut_10(
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
    masked_cmd = mask_command(None)
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
            "✅ Command completed",
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


def x_run__mutmut_11(
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
    log.trace(None, command=masked_cmd, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_12(
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
    log.trace("🚀 Running command", command=None, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_13(
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
    log.trace("🚀 Running command", command=masked_cmd, cwd=None)

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
            "✅ Command completed",
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


def x_run__mutmut_14(
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
    log.trace(command=masked_cmd, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_15(
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
    log.trace("🚀 Running command", cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_16(
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
    log.trace(
        "🚀 Running command",
        command=masked_cmd,
    )

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
            "✅ Command completed",
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


def x_run__mutmut_17(
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
    log.trace("XX🚀 Running commandXX", command=masked_cmd, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_18(
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
    log.trace("🚀 running command", command=masked_cmd, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_19(
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
    log.trace("🚀 RUNNING COMMAND", command=masked_cmd, cwd=str(cwd) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_20(
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
    log.trace("🚀 Running command", command=masked_cmd, cwd=str(None) if cwd else None)

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
            "✅ Command completed",
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


def x_run__mutmut_21(
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
    validate_command_type(None, shell)

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
            "✅ Command completed",
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


def x_run__mutmut_22(
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
    validate_command_type(cmd, None)

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
            "✅ Command completed",
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


def x_run__mutmut_23(
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
    validate_command_type(shell)

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
            "✅ Command completed",
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


def x_run__mutmut_24(
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
    validate_command_type(
        cmd,
    )

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
            "✅ Command completed",
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


def x_run__mutmut_25(
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
    run_env = None

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
            "✅ Command completed",
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


def x_run__mutmut_26(
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
    run_env = prepare_environment(None)

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
            "✅ Command completed",
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


def x_run__mutmut_27(
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
    cwd = None

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
            "✅ Command completed",
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


def x_run__mutmut_28(
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
    cwd = normalize_cwd(None)

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
            "✅ Command completed",
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


def x_run__mutmut_29(
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
    subprocess_input = None

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
            "✅ Command completed",
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


def x_run__mutmut_30(
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
    subprocess_input = prepare_input(None, text)

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
            "✅ Command completed",
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


def x_run__mutmut_31(
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
    subprocess_input = prepare_input(input, None)

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
            "✅ Command completed",
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


def x_run__mutmut_32(
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
    subprocess_input = prepare_input(text)

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
            "✅ Command completed",
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


def x_run__mutmut_33(
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
    subprocess_input = prepare_input(
        input,
    )

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
            "✅ Command completed",
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


def x_run__mutmut_34(
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
        subprocess_cmd = None

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
            "✅ Command completed",
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


def x_run__mutmut_35(
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

        result = None

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
            "✅ Command completed",
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


def x_run__mutmut_36(
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
            None,
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
            "✅ Command completed",
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


def x_run__mutmut_37(
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
            cwd=None,
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
            "✅ Command completed",
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


def x_run__mutmut_38(
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
            env=None,
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
            "✅ Command completed",
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


def x_run__mutmut_39(
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
            capture_output=None,
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
            "✅ Command completed",
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


def x_run__mutmut_40(
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
            text=None,
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
            "✅ Command completed",
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


def x_run__mutmut_41(
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
            input=None,
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
            "✅ Command completed",
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


def x_run__mutmut_42(
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
            timeout=None,
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
            "✅ Command completed",
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


def x_run__mutmut_43(
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
            check=None,  # We'll handle the check ourselves
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
            "✅ Command completed",
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


def x_run__mutmut_44(
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
            shell=None,  # nosec B602 - Shell usage validated by caller context
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
            "✅ Command completed",
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


def x_run__mutmut_45(
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
            "✅ Command completed",
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


def x_run__mutmut_46(
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
            "✅ Command completed",
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


def x_run__mutmut_47(
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
            "✅ Command completed",
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


def x_run__mutmut_48(
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
            "✅ Command completed",
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


def x_run__mutmut_49(
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
            "✅ Command completed",
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


def x_run__mutmut_50(
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
            "✅ Command completed",
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


def x_run__mutmut_51(
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
            "✅ Command completed",
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


def x_run__mutmut_52(
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
            "✅ Command completed",
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


def x_run__mutmut_53(
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
            "✅ Command completed",
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


def x_run__mutmut_54(
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
            "✅ Command completed",
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


def x_run__mutmut_55(
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
            check=True,  # We'll handle the check ourselves
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
            "✅ Command completed",
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


def x_run__mutmut_56(
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

        completed = None

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
            "✅ Command completed",
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


def x_run__mutmut_57(
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
            args=None,
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
            "✅ Command completed",
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


def x_run__mutmut_58(
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
            returncode=None,
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
            "✅ Command completed",
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


def x_run__mutmut_59(
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
            stdout=None,
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
            "✅ Command completed",
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


def x_run__mutmut_60(
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
            stderr=None,
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
            "✅ Command completed",
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


def x_run__mutmut_61(
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
            cwd=None,
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
            "✅ Command completed",
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


def x_run__mutmut_62(
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
            env=None,  # Only store caller overrides, not full run_env
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
            "✅ Command completed",
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


def x_run__mutmut_63(
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
            "✅ Command completed",
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


def x_run__mutmut_64(
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
            "✅ Command completed",
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


def x_run__mutmut_65(
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
            "✅ Command completed",
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


def x_run__mutmut_66(
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
            "✅ Command completed",
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


def x_run__mutmut_67(
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
            "✅ Command completed",
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


def x_run__mutmut_68(
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
            "✅ Command completed",
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


def x_run__mutmut_69(
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
            stdout=result.stdout if capture_output else "XXXX",
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
            "✅ Command completed",
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


def x_run__mutmut_70(
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
            stderr=result.stderr if capture_output else "XXXX",
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
            "✅ Command completed",
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


def x_run__mutmut_71(
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
            env=dict(None) if env else None,  # Only store caller overrides, not full run_env
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
            "✅ Command completed",
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


def x_run__mutmut_72(
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

        if check or result.returncode != 0:
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
            "✅ Command completed",
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


def x_run__mutmut_73(
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

        if check and result.returncode == 0:
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
            "✅ Command completed",
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


def x_run__mutmut_74(
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

        if check and result.returncode != 1:
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
            "✅ Command completed",
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


def x_run__mutmut_75(
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
                None,
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
            "✅ Command completed",
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


def x_run__mutmut_76(
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
                command=None,
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
            "✅ Command completed",
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


def x_run__mutmut_77(
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
                returncode=None,
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
            "✅ Command completed",
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


def x_run__mutmut_78(
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
                stderr=None,
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
            "✅ Command completed",
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


def x_run__mutmut_79(
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
            "✅ Command completed",
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


def x_run__mutmut_80(
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
            "✅ Command completed",
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


def x_run__mutmut_81(
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
            "✅ Command completed",
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


def x_run__mutmut_82(
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
            "✅ Command completed",
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


def x_run__mutmut_83(
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
                "XX❌ Command failedXX",
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
            "✅ Command completed",
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


def x_run__mutmut_84(
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
                "❌ command failed",
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
            "✅ Command completed",
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


def x_run__mutmut_85(
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
                "❌ COMMAND FAILED",
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
            "✅ Command completed",
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


def x_run__mutmut_86(
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
                None,
                code="PROCESS_COMMAND_FAILED",
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_87(
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
                code=None,
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_88(
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
                command=None,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_89(
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
                return_code=None,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_90(
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
                stdout=None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_91(
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
                stderr=None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_92(
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
                code="PROCESS_COMMAND_FAILED",
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_93(
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
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_94(
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
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_95(
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
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_96(
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
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_97(
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
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_98(
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
                code="XXPROCESS_COMMAND_FAILEDXX",
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_99(
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
                code="process_command_failed",
                command=cmd_str,
                return_code=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        log.debug(
            "✅ Command completed",
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


def x_run__mutmut_100(
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
            None,
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


def x_run__mutmut_101(
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
            "✅ Command completed",
            command=None,
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


def x_run__mutmut_102(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=None,
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


def x_run__mutmut_103(
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


def x_run__mutmut_104(
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
            "✅ Command completed",
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


def x_run__mutmut_105(
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
            "✅ Command completed",
            command=cmd_str,
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


def x_run__mutmut_106(
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
            "XX✅ Command completedXX",
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


def x_run__mutmut_107(
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
            "✅ command completed",
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


def x_run__mutmut_108(
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
            "✅ COMMAND COMPLETED",
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


def x_run__mutmut_109(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            None,
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


def x_run__mutmut_110(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ Command timed out",
            command=None,
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


def x_run__mutmut_111(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ Command timed out",
            command=cmd_str,
            timeout=None,
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


def x_run__mutmut_112(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
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


def x_run__mutmut_113(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ Command timed out",
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


def x_run__mutmut_114(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ Command timed out",
            command=cmd_str,
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


def x_run__mutmut_115(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "XX⏱️ Command timed outXX",
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


def x_run__mutmut_116(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ command timed out",
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


def x_run__mutmut_117(
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
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        log.error(
            "⏱️ COMMAND TIMED OUT",
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


def x_run__mutmut_118(
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
            "✅ Command completed",
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
            None,
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


def x_run__mutmut_119(
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
            "✅ Command completed",
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
            code=None,
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


def x_run__mutmut_120(
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
            "✅ Command completed",
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
            command=None,
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


def x_run__mutmut_121(
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
            "✅ Command completed",
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
            timeout_seconds=None,
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


def x_run__mutmut_122(
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
            "✅ Command completed",
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


def x_run__mutmut_123(
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
            "✅ Command completed",
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


def x_run__mutmut_124(
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
            "✅ Command completed",
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


def x_run__mutmut_125(
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
            "✅ Command completed",
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


def x_run__mutmut_126(
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
            "✅ Command completed",
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
            code="XXPROCESS_TIMEOUTXX",
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


def x_run__mutmut_127(
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
            "✅ Command completed",
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
            code="process_timeout",
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


def x_run__mutmut_128(
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
            "✅ Command completed",
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
            None,
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_129(
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
            "✅ Command completed",
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
            command=None,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_130(
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
            "✅ Command completed",
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
            error=None,
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_131(
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
            "✅ Command completed",
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
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_132(
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
            "✅ Command completed",
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
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_133(
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
            "✅ Command completed",
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
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_134(
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
            "✅ Command completed",
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
            "XX💥 Command execution failedXX",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_135(
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
            "✅ Command completed",
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
            "💥 command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_136(
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
            "✅ Command completed",
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
            "💥 COMMAND EXECUTION FAILED",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_137(
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
            "✅ Command completed",
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
            error=str(None),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_138(
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
            "✅ Command completed",
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
            None,
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_139(
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
            "✅ Command completed",
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
            code=None,
            command=cmd_str,
        ) from e


def x_run__mutmut_140(
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
            "✅ Command completed",
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
            command=None,
        ) from e


def x_run__mutmut_141(
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
            "✅ Command completed",
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
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


def x_run__mutmut_142(
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
            "✅ Command completed",
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
            command=cmd_str,
        ) from e


def x_run__mutmut_143(
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
            "✅ Command completed",
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
        ) from e


def x_run__mutmut_144(
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
            "✅ Command completed",
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
            code="XXPROCESS_EXECUTION_FAILEDXX",
            command=cmd_str,
        ) from e


def x_run__mutmut_145(
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
            "✅ Command completed",
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
            code="process_execution_failed",
            command=cmd_str,
        ) from e


x_run__mutmut_mutants: ClassVar[MutantDict] = {
    "x_run__mutmut_1": x_run__mutmut_1,
    "x_run__mutmut_2": x_run__mutmut_2,
    "x_run__mutmut_3": x_run__mutmut_3,
    "x_run__mutmut_4": x_run__mutmut_4,
    "x_run__mutmut_5": x_run__mutmut_5,
    "x_run__mutmut_6": x_run__mutmut_6,
    "x_run__mutmut_7": x_run__mutmut_7,
    "x_run__mutmut_8": x_run__mutmut_8,
    "x_run__mutmut_9": x_run__mutmut_9,
    "x_run__mutmut_10": x_run__mutmut_10,
    "x_run__mutmut_11": x_run__mutmut_11,
    "x_run__mutmut_12": x_run__mutmut_12,
    "x_run__mutmut_13": x_run__mutmut_13,
    "x_run__mutmut_14": x_run__mutmut_14,
    "x_run__mutmut_15": x_run__mutmut_15,
    "x_run__mutmut_16": x_run__mutmut_16,
    "x_run__mutmut_17": x_run__mutmut_17,
    "x_run__mutmut_18": x_run__mutmut_18,
    "x_run__mutmut_19": x_run__mutmut_19,
    "x_run__mutmut_20": x_run__mutmut_20,
    "x_run__mutmut_21": x_run__mutmut_21,
    "x_run__mutmut_22": x_run__mutmut_22,
    "x_run__mutmut_23": x_run__mutmut_23,
    "x_run__mutmut_24": x_run__mutmut_24,
    "x_run__mutmut_25": x_run__mutmut_25,
    "x_run__mutmut_26": x_run__mutmut_26,
    "x_run__mutmut_27": x_run__mutmut_27,
    "x_run__mutmut_28": x_run__mutmut_28,
    "x_run__mutmut_29": x_run__mutmut_29,
    "x_run__mutmut_30": x_run__mutmut_30,
    "x_run__mutmut_31": x_run__mutmut_31,
    "x_run__mutmut_32": x_run__mutmut_32,
    "x_run__mutmut_33": x_run__mutmut_33,
    "x_run__mutmut_34": x_run__mutmut_34,
    "x_run__mutmut_35": x_run__mutmut_35,
    "x_run__mutmut_36": x_run__mutmut_36,
    "x_run__mutmut_37": x_run__mutmut_37,
    "x_run__mutmut_38": x_run__mutmut_38,
    "x_run__mutmut_39": x_run__mutmut_39,
    "x_run__mutmut_40": x_run__mutmut_40,
    "x_run__mutmut_41": x_run__mutmut_41,
    "x_run__mutmut_42": x_run__mutmut_42,
    "x_run__mutmut_43": x_run__mutmut_43,
    "x_run__mutmut_44": x_run__mutmut_44,
    "x_run__mutmut_45": x_run__mutmut_45,
    "x_run__mutmut_46": x_run__mutmut_46,
    "x_run__mutmut_47": x_run__mutmut_47,
    "x_run__mutmut_48": x_run__mutmut_48,
    "x_run__mutmut_49": x_run__mutmut_49,
    "x_run__mutmut_50": x_run__mutmut_50,
    "x_run__mutmut_51": x_run__mutmut_51,
    "x_run__mutmut_52": x_run__mutmut_52,
    "x_run__mutmut_53": x_run__mutmut_53,
    "x_run__mutmut_54": x_run__mutmut_54,
    "x_run__mutmut_55": x_run__mutmut_55,
    "x_run__mutmut_56": x_run__mutmut_56,
    "x_run__mutmut_57": x_run__mutmut_57,
    "x_run__mutmut_58": x_run__mutmut_58,
    "x_run__mutmut_59": x_run__mutmut_59,
    "x_run__mutmut_60": x_run__mutmut_60,
    "x_run__mutmut_61": x_run__mutmut_61,
    "x_run__mutmut_62": x_run__mutmut_62,
    "x_run__mutmut_63": x_run__mutmut_63,
    "x_run__mutmut_64": x_run__mutmut_64,
    "x_run__mutmut_65": x_run__mutmut_65,
    "x_run__mutmut_66": x_run__mutmut_66,
    "x_run__mutmut_67": x_run__mutmut_67,
    "x_run__mutmut_68": x_run__mutmut_68,
    "x_run__mutmut_69": x_run__mutmut_69,
    "x_run__mutmut_70": x_run__mutmut_70,
    "x_run__mutmut_71": x_run__mutmut_71,
    "x_run__mutmut_72": x_run__mutmut_72,
    "x_run__mutmut_73": x_run__mutmut_73,
    "x_run__mutmut_74": x_run__mutmut_74,
    "x_run__mutmut_75": x_run__mutmut_75,
    "x_run__mutmut_76": x_run__mutmut_76,
    "x_run__mutmut_77": x_run__mutmut_77,
    "x_run__mutmut_78": x_run__mutmut_78,
    "x_run__mutmut_79": x_run__mutmut_79,
    "x_run__mutmut_80": x_run__mutmut_80,
    "x_run__mutmut_81": x_run__mutmut_81,
    "x_run__mutmut_82": x_run__mutmut_82,
    "x_run__mutmut_83": x_run__mutmut_83,
    "x_run__mutmut_84": x_run__mutmut_84,
    "x_run__mutmut_85": x_run__mutmut_85,
    "x_run__mutmut_86": x_run__mutmut_86,
    "x_run__mutmut_87": x_run__mutmut_87,
    "x_run__mutmut_88": x_run__mutmut_88,
    "x_run__mutmut_89": x_run__mutmut_89,
    "x_run__mutmut_90": x_run__mutmut_90,
    "x_run__mutmut_91": x_run__mutmut_91,
    "x_run__mutmut_92": x_run__mutmut_92,
    "x_run__mutmut_93": x_run__mutmut_93,
    "x_run__mutmut_94": x_run__mutmut_94,
    "x_run__mutmut_95": x_run__mutmut_95,
    "x_run__mutmut_96": x_run__mutmut_96,
    "x_run__mutmut_97": x_run__mutmut_97,
    "x_run__mutmut_98": x_run__mutmut_98,
    "x_run__mutmut_99": x_run__mutmut_99,
    "x_run__mutmut_100": x_run__mutmut_100,
    "x_run__mutmut_101": x_run__mutmut_101,
    "x_run__mutmut_102": x_run__mutmut_102,
    "x_run__mutmut_103": x_run__mutmut_103,
    "x_run__mutmut_104": x_run__mutmut_104,
    "x_run__mutmut_105": x_run__mutmut_105,
    "x_run__mutmut_106": x_run__mutmut_106,
    "x_run__mutmut_107": x_run__mutmut_107,
    "x_run__mutmut_108": x_run__mutmut_108,
    "x_run__mutmut_109": x_run__mutmut_109,
    "x_run__mutmut_110": x_run__mutmut_110,
    "x_run__mutmut_111": x_run__mutmut_111,
    "x_run__mutmut_112": x_run__mutmut_112,
    "x_run__mutmut_113": x_run__mutmut_113,
    "x_run__mutmut_114": x_run__mutmut_114,
    "x_run__mutmut_115": x_run__mutmut_115,
    "x_run__mutmut_116": x_run__mutmut_116,
    "x_run__mutmut_117": x_run__mutmut_117,
    "x_run__mutmut_118": x_run__mutmut_118,
    "x_run__mutmut_119": x_run__mutmut_119,
    "x_run__mutmut_120": x_run__mutmut_120,
    "x_run__mutmut_121": x_run__mutmut_121,
    "x_run__mutmut_122": x_run__mutmut_122,
    "x_run__mutmut_123": x_run__mutmut_123,
    "x_run__mutmut_124": x_run__mutmut_124,
    "x_run__mutmut_125": x_run__mutmut_125,
    "x_run__mutmut_126": x_run__mutmut_126,
    "x_run__mutmut_127": x_run__mutmut_127,
    "x_run__mutmut_128": x_run__mutmut_128,
    "x_run__mutmut_129": x_run__mutmut_129,
    "x_run__mutmut_130": x_run__mutmut_130,
    "x_run__mutmut_131": x_run__mutmut_131,
    "x_run__mutmut_132": x_run__mutmut_132,
    "x_run__mutmut_133": x_run__mutmut_133,
    "x_run__mutmut_134": x_run__mutmut_134,
    "x_run__mutmut_135": x_run__mutmut_135,
    "x_run__mutmut_136": x_run__mutmut_136,
    "x_run__mutmut_137": x_run__mutmut_137,
    "x_run__mutmut_138": x_run__mutmut_138,
    "x_run__mutmut_139": x_run__mutmut_139,
    "x_run__mutmut_140": x_run__mutmut_140,
    "x_run__mutmut_141": x_run__mutmut_141,
    "x_run__mutmut_142": x_run__mutmut_142,
    "x_run__mutmut_143": x_run__mutmut_143,
    "x_run__mutmut_144": x_run__mutmut_144,
    "x_run__mutmut_145": x_run__mutmut_145,
}


def run(*args, **kwargs):
    result = _mutmut_trampoline(x_run__mutmut_orig, x_run__mutmut_mutants, args, kwargs)
    return result


run.__signature__ = _mutmut_signature(x_run__mutmut_orig)
x_run__mutmut_orig.__name__ = "x_run"


def x_run_simple__mutmut_orig(
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


def x_run_simple__mutmut_1(
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
    result = None
    return result.stdout.strip()


def x_run_simple__mutmut_2(
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
    result = run(None, cwd=cwd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_3(
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
    result = run(cmd, cwd=None, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_4(
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
    result = run(cmd, cwd=cwd, capture_output=None, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_5(
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
    result = run(cmd, cwd=cwd, capture_output=True, check=None, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_6(
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
    result = run(cwd=cwd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_7(
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
    result = run(cmd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_8(
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
    result = run(cmd, cwd=cwd, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_9(
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
    result = run(cmd, cwd=cwd, capture_output=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_10(
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
    result = run(
        cmd,
        cwd=cwd,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def x_run_simple__mutmut_11(
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
    result = run(cmd, cwd=cwd, capture_output=False, check=True, **kwargs)
    return result.stdout.strip()


def x_run_simple__mutmut_12(
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
    result = run(cmd, cwd=cwd, capture_output=True, check=False, **kwargs)
    return result.stdout.strip()


x_run_simple__mutmut_mutants: ClassVar[MutantDict] = {
    "x_run_simple__mutmut_1": x_run_simple__mutmut_1,
    "x_run_simple__mutmut_2": x_run_simple__mutmut_2,
    "x_run_simple__mutmut_3": x_run_simple__mutmut_3,
    "x_run_simple__mutmut_4": x_run_simple__mutmut_4,
    "x_run_simple__mutmut_5": x_run_simple__mutmut_5,
    "x_run_simple__mutmut_6": x_run_simple__mutmut_6,
    "x_run_simple__mutmut_7": x_run_simple__mutmut_7,
    "x_run_simple__mutmut_8": x_run_simple__mutmut_8,
    "x_run_simple__mutmut_9": x_run_simple__mutmut_9,
    "x_run_simple__mutmut_10": x_run_simple__mutmut_10,
    "x_run_simple__mutmut_11": x_run_simple__mutmut_11,
    "x_run_simple__mutmut_12": x_run_simple__mutmut_12,
}


def run_simple(*args, **kwargs):
    result = _mutmut_trampoline(x_run_simple__mutmut_orig, x_run_simple__mutmut_mutants, args, kwargs)
    return result


run_simple.__signature__ = _mutmut_signature(x_run_simple__mutmut_orig)
x_run_simple__mutmut_orig.__name__ = "x_run_simple"


# <3 🧱🤝🏃🪄
