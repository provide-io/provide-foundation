# provide/foundation/errors/process.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# provide/foundation/errors/process.py
#
from typing import Any

from provide.foundation.errors.base import FoundationError

"""Process execution related errors."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ProcessError(FoundationError):
    """Error for external process execution failures with output capture."""

    def xǁProcessErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = True,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = None

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = None
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(None)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else "XX XX".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message = f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message -= f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message = f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message -= f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message = "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message -= "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "XX\nProcess timed outXX"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nprocess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nPROCESS TIMED OUT"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = None
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode(None, "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", None) if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", ) if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("XXutf-8XX", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("UTF-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "XXreplaceXX") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "REPLACE") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message = f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message -= f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = None
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode(None, "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", None) if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_31(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", ) if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_32(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("XXutf-8XX", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_33(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("UTF-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_34(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "XXreplaceXX") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_35(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "REPLACE") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_36(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message = f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_37(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message -= f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_38(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = None
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_39(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            None,
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_40(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "XXprocess.commandXX": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_41(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "PROCESS.COMMAND": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_42(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "XXprocess.return_codeXX": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_43(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "PROCESS.RETURN_CODE": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_44(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "XXprocess.timeoutXX": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_45(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "PROCESS.TIMEOUT": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_46(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = None

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_47(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode(None, "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_48(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", None).strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_49(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_50(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", ).strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_51(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("XXutf-8XX", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_52(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("UTF-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_53(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "XXreplaceXX").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_54(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "REPLACE").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_55(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = None

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_56(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode(None, "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_57(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", None).strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_58(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_59(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", ).strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_60(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("XXutf-8XX", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_61(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("UTF-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_62(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "XXreplaceXX").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_63(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "REPLACE").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_64(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = None
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_65(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = None
        self.timeout = timeout

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_66(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = None

        super().__init__(full_message, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_67(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(None, code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_68(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=None, context=context)

    def xǁProcessErrorǁ__init____mutmut_69(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, context=None)

    def xǁProcessErrorǁ__init____mutmut_70(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(code=code, context=context)

    def xǁProcessErrorǁ__init____mutmut_71(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, context=context)

    def xǁProcessErrorǁ__init____mutmut_72(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        return_code: int | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        timeout: bool = False,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        """Initialize ProcessError with command execution details.

        Args:
            message: Human-readable error message
            command: The command that was executed
            return_code: Process return/exit code
            stdout: Standard output from the process
            stderr: Standard error from the process
            timeout: Whether the process timed out
            code: Optional error code
            **extra_context: Additional context information

        """
        # Build comprehensive error message
        full_message = message

        if command:
            cmd_str = command if isinstance(command, str) else " ".join(command)
            full_message += f"\nCommand: {cmd_str}"

        if return_code is not None:
            full_message += f"\nReturn code: {return_code}"

        if timeout:
            full_message += "\nProcess timed out"

        if stdout:
            stdout_str = stdout.decode("utf-8", "replace") if isinstance(stdout, bytes) else stdout
            if stdout_str.strip():
                full_message += f"\n--- STDOUT ---\n{stdout_str.strip()}"

        if stderr:
            stderr_str = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else stderr
            if stderr_str.strip():
                full_message += f"\n--- STDERR ---\n{stderr_str.strip()}"

        # Store structured data
        context = extra_context.copy()
        context.update(
            {
                "process.command": command,
                "process.return_code": return_code,
                "process.timeout": timeout,
            },
        )

        # Store clean stdout/stderr for programmatic access
        self.stdout = (
            stdout.decode("utf-8", "replace").strip()
            if isinstance(stdout, bytes)
            else stdout.strip()
            if stdout
            else None
        )

        self.stderr = (
            stderr.decode("utf-8", "replace").strip()
            if isinstance(stderr, bytes)
            else stderr.strip()
            if stderr
            else None
        )

        self.command = command
        self.return_code = return_code
        self.timeout = timeout

        super().__init__(full_message, code=code, )
    
    xǁProcessErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProcessErrorǁ__init____mutmut_1': xǁProcessErrorǁ__init____mutmut_1, 
        'xǁProcessErrorǁ__init____mutmut_2': xǁProcessErrorǁ__init____mutmut_2, 
        'xǁProcessErrorǁ__init____mutmut_3': xǁProcessErrorǁ__init____mutmut_3, 
        'xǁProcessErrorǁ__init____mutmut_4': xǁProcessErrorǁ__init____mutmut_4, 
        'xǁProcessErrorǁ__init____mutmut_5': xǁProcessErrorǁ__init____mutmut_5, 
        'xǁProcessErrorǁ__init____mutmut_6': xǁProcessErrorǁ__init____mutmut_6, 
        'xǁProcessErrorǁ__init____mutmut_7': xǁProcessErrorǁ__init____mutmut_7, 
        'xǁProcessErrorǁ__init____mutmut_8': xǁProcessErrorǁ__init____mutmut_8, 
        'xǁProcessErrorǁ__init____mutmut_9': xǁProcessErrorǁ__init____mutmut_9, 
        'xǁProcessErrorǁ__init____mutmut_10': xǁProcessErrorǁ__init____mutmut_10, 
        'xǁProcessErrorǁ__init____mutmut_11': xǁProcessErrorǁ__init____mutmut_11, 
        'xǁProcessErrorǁ__init____mutmut_12': xǁProcessErrorǁ__init____mutmut_12, 
        'xǁProcessErrorǁ__init____mutmut_13': xǁProcessErrorǁ__init____mutmut_13, 
        'xǁProcessErrorǁ__init____mutmut_14': xǁProcessErrorǁ__init____mutmut_14, 
        'xǁProcessErrorǁ__init____mutmut_15': xǁProcessErrorǁ__init____mutmut_15, 
        'xǁProcessErrorǁ__init____mutmut_16': xǁProcessErrorǁ__init____mutmut_16, 
        'xǁProcessErrorǁ__init____mutmut_17': xǁProcessErrorǁ__init____mutmut_17, 
        'xǁProcessErrorǁ__init____mutmut_18': xǁProcessErrorǁ__init____mutmut_18, 
        'xǁProcessErrorǁ__init____mutmut_19': xǁProcessErrorǁ__init____mutmut_19, 
        'xǁProcessErrorǁ__init____mutmut_20': xǁProcessErrorǁ__init____mutmut_20, 
        'xǁProcessErrorǁ__init____mutmut_21': xǁProcessErrorǁ__init____mutmut_21, 
        'xǁProcessErrorǁ__init____mutmut_22': xǁProcessErrorǁ__init____mutmut_22, 
        'xǁProcessErrorǁ__init____mutmut_23': xǁProcessErrorǁ__init____mutmut_23, 
        'xǁProcessErrorǁ__init____mutmut_24': xǁProcessErrorǁ__init____mutmut_24, 
        'xǁProcessErrorǁ__init____mutmut_25': xǁProcessErrorǁ__init____mutmut_25, 
        'xǁProcessErrorǁ__init____mutmut_26': xǁProcessErrorǁ__init____mutmut_26, 
        'xǁProcessErrorǁ__init____mutmut_27': xǁProcessErrorǁ__init____mutmut_27, 
        'xǁProcessErrorǁ__init____mutmut_28': xǁProcessErrorǁ__init____mutmut_28, 
        'xǁProcessErrorǁ__init____mutmut_29': xǁProcessErrorǁ__init____mutmut_29, 
        'xǁProcessErrorǁ__init____mutmut_30': xǁProcessErrorǁ__init____mutmut_30, 
        'xǁProcessErrorǁ__init____mutmut_31': xǁProcessErrorǁ__init____mutmut_31, 
        'xǁProcessErrorǁ__init____mutmut_32': xǁProcessErrorǁ__init____mutmut_32, 
        'xǁProcessErrorǁ__init____mutmut_33': xǁProcessErrorǁ__init____mutmut_33, 
        'xǁProcessErrorǁ__init____mutmut_34': xǁProcessErrorǁ__init____mutmut_34, 
        'xǁProcessErrorǁ__init____mutmut_35': xǁProcessErrorǁ__init____mutmut_35, 
        'xǁProcessErrorǁ__init____mutmut_36': xǁProcessErrorǁ__init____mutmut_36, 
        'xǁProcessErrorǁ__init____mutmut_37': xǁProcessErrorǁ__init____mutmut_37, 
        'xǁProcessErrorǁ__init____mutmut_38': xǁProcessErrorǁ__init____mutmut_38, 
        'xǁProcessErrorǁ__init____mutmut_39': xǁProcessErrorǁ__init____mutmut_39, 
        'xǁProcessErrorǁ__init____mutmut_40': xǁProcessErrorǁ__init____mutmut_40, 
        'xǁProcessErrorǁ__init____mutmut_41': xǁProcessErrorǁ__init____mutmut_41, 
        'xǁProcessErrorǁ__init____mutmut_42': xǁProcessErrorǁ__init____mutmut_42, 
        'xǁProcessErrorǁ__init____mutmut_43': xǁProcessErrorǁ__init____mutmut_43, 
        'xǁProcessErrorǁ__init____mutmut_44': xǁProcessErrorǁ__init____mutmut_44, 
        'xǁProcessErrorǁ__init____mutmut_45': xǁProcessErrorǁ__init____mutmut_45, 
        'xǁProcessErrorǁ__init____mutmut_46': xǁProcessErrorǁ__init____mutmut_46, 
        'xǁProcessErrorǁ__init____mutmut_47': xǁProcessErrorǁ__init____mutmut_47, 
        'xǁProcessErrorǁ__init____mutmut_48': xǁProcessErrorǁ__init____mutmut_48, 
        'xǁProcessErrorǁ__init____mutmut_49': xǁProcessErrorǁ__init____mutmut_49, 
        'xǁProcessErrorǁ__init____mutmut_50': xǁProcessErrorǁ__init____mutmut_50, 
        'xǁProcessErrorǁ__init____mutmut_51': xǁProcessErrorǁ__init____mutmut_51, 
        'xǁProcessErrorǁ__init____mutmut_52': xǁProcessErrorǁ__init____mutmut_52, 
        'xǁProcessErrorǁ__init____mutmut_53': xǁProcessErrorǁ__init____mutmut_53, 
        'xǁProcessErrorǁ__init____mutmut_54': xǁProcessErrorǁ__init____mutmut_54, 
        'xǁProcessErrorǁ__init____mutmut_55': xǁProcessErrorǁ__init____mutmut_55, 
        'xǁProcessErrorǁ__init____mutmut_56': xǁProcessErrorǁ__init____mutmut_56, 
        'xǁProcessErrorǁ__init____mutmut_57': xǁProcessErrorǁ__init____mutmut_57, 
        'xǁProcessErrorǁ__init____mutmut_58': xǁProcessErrorǁ__init____mutmut_58, 
        'xǁProcessErrorǁ__init____mutmut_59': xǁProcessErrorǁ__init____mutmut_59, 
        'xǁProcessErrorǁ__init____mutmut_60': xǁProcessErrorǁ__init____mutmut_60, 
        'xǁProcessErrorǁ__init____mutmut_61': xǁProcessErrorǁ__init____mutmut_61, 
        'xǁProcessErrorǁ__init____mutmut_62': xǁProcessErrorǁ__init____mutmut_62, 
        'xǁProcessErrorǁ__init____mutmut_63': xǁProcessErrorǁ__init____mutmut_63, 
        'xǁProcessErrorǁ__init____mutmut_64': xǁProcessErrorǁ__init____mutmut_64, 
        'xǁProcessErrorǁ__init____mutmut_65': xǁProcessErrorǁ__init____mutmut_65, 
        'xǁProcessErrorǁ__init____mutmut_66': xǁProcessErrorǁ__init____mutmut_66, 
        'xǁProcessErrorǁ__init____mutmut_67': xǁProcessErrorǁ__init____mutmut_67, 
        'xǁProcessErrorǁ__init____mutmut_68': xǁProcessErrorǁ__init____mutmut_68, 
        'xǁProcessErrorǁ__init____mutmut_69': xǁProcessErrorǁ__init____mutmut_69, 
        'xǁProcessErrorǁ__init____mutmut_70': xǁProcessErrorǁ__init____mutmut_70, 
        'xǁProcessErrorǁ__init____mutmut_71': xǁProcessErrorǁ__init____mutmut_71, 
        'xǁProcessErrorǁ__init____mutmut_72': xǁProcessErrorǁ__init____mutmut_72
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProcessErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProcessErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProcessErrorǁ__init____mutmut_orig)
    xǁProcessErrorǁ__init____mutmut_orig.__name__ = 'xǁProcessErrorǁ__init__'

    def xǁProcessErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for process errors."""
        return "PROCESS_ERROR"

    def xǁProcessErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for process errors."""
        return "XXPROCESS_ERRORXX"

    def xǁProcessErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for process errors."""
        return "process_error"
    
    xǁProcessErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProcessErrorǁ_default_code__mutmut_1': xǁProcessErrorǁ_default_code__mutmut_1, 
        'xǁProcessErrorǁ_default_code__mutmut_2': xǁProcessErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProcessErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁProcessErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁProcessErrorǁ_default_code__mutmut_orig)
    xǁProcessErrorǁ_default_code__mutmut_orig.__name__ = 'xǁProcessErrorǁ_default_code'


class CommandNotFoundError(ProcessError):
    """Error when a command/executable is not found."""

    def xǁCommandNotFoundErrorǁ_default_code__mutmut_orig(self) -> str:
        return "COMMAND_NOT_FOUND"

    def xǁCommandNotFoundErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCOMMAND_NOT_FOUNDXX"

    def xǁCommandNotFoundErrorǁ_default_code__mutmut_2(self) -> str:
        return "command_not_found"
    
    xǁCommandNotFoundErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCommandNotFoundErrorǁ_default_code__mutmut_1': xǁCommandNotFoundErrorǁ_default_code__mutmut_1, 
        'xǁCommandNotFoundErrorǁ_default_code__mutmut_2': xǁCommandNotFoundErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCommandNotFoundErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁCommandNotFoundErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁCommandNotFoundErrorǁ_default_code__mutmut_orig)
    xǁCommandNotFoundErrorǁ_default_code__mutmut_orig.__name__ = 'xǁCommandNotFoundErrorǁ_default_code'


class ProcessTimeoutError(ProcessError):
    """Error when a process times out."""

    def xǁProcessTimeoutErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = None
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = None

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["XXprocess.timeout_secondsXX"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["PROCESS.TIMEOUT_SECONDS"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            None,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=None,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=None,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=None,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=None,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=None,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stderr=stderr,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            timeout=True,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            code=code,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            **context,
        )

    def xǁProcessTimeoutErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=True,
            code=code,
            )

    def xǁProcessTimeoutErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        command: str | list[str] | None = None,
        timeout_seconds: float | None = None,
        stdout: str | bytes | None = None,
        stderr: str | bytes | None = None,
        code: str | None = None,
        **extra_context: Any,
    ) -> None:
        context = extra_context.copy()
        if timeout_seconds is not None:
            context["process.timeout_seconds"] = timeout_seconds

        super().__init__(
            message,
            command=command,
            stdout=stdout,
            stderr=stderr,
            timeout=False,
            code=code,
            **context,
        )
    
    xǁProcessTimeoutErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProcessTimeoutErrorǁ__init____mutmut_1': xǁProcessTimeoutErrorǁ__init____mutmut_1, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_2': xǁProcessTimeoutErrorǁ__init____mutmut_2, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_3': xǁProcessTimeoutErrorǁ__init____mutmut_3, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_4': xǁProcessTimeoutErrorǁ__init____mutmut_4, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_5': xǁProcessTimeoutErrorǁ__init____mutmut_5, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_6': xǁProcessTimeoutErrorǁ__init____mutmut_6, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_7': xǁProcessTimeoutErrorǁ__init____mutmut_7, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_8': xǁProcessTimeoutErrorǁ__init____mutmut_8, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_9': xǁProcessTimeoutErrorǁ__init____mutmut_9, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_10': xǁProcessTimeoutErrorǁ__init____mutmut_10, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_11': xǁProcessTimeoutErrorǁ__init____mutmut_11, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_12': xǁProcessTimeoutErrorǁ__init____mutmut_12, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_13': xǁProcessTimeoutErrorǁ__init____mutmut_13, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_14': xǁProcessTimeoutErrorǁ__init____mutmut_14, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_15': xǁProcessTimeoutErrorǁ__init____mutmut_15, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_16': xǁProcessTimeoutErrorǁ__init____mutmut_16, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_17': xǁProcessTimeoutErrorǁ__init____mutmut_17, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_18': xǁProcessTimeoutErrorǁ__init____mutmut_18, 
        'xǁProcessTimeoutErrorǁ__init____mutmut_19': xǁProcessTimeoutErrorǁ__init____mutmut_19
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProcessTimeoutErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProcessTimeoutErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProcessTimeoutErrorǁ__init____mutmut_orig)
    xǁProcessTimeoutErrorǁ__init____mutmut_orig.__name__ = 'xǁProcessTimeoutErrorǁ__init__'

    def xǁProcessTimeoutErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PROCESS_TIMEOUT"

    def xǁProcessTimeoutErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPROCESS_TIMEOUTXX"

    def xǁProcessTimeoutErrorǁ_default_code__mutmut_2(self) -> str:
        return "process_timeout"
    
    xǁProcessTimeoutErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProcessTimeoutErrorǁ_default_code__mutmut_1': xǁProcessTimeoutErrorǁ_default_code__mutmut_1, 
        'xǁProcessTimeoutErrorǁ_default_code__mutmut_2': xǁProcessTimeoutErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProcessTimeoutErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁProcessTimeoutErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁProcessTimeoutErrorǁ_default_code__mutmut_orig)
    xǁProcessTimeoutErrorǁ_default_code__mutmut_orig.__name__ = 'xǁProcessTimeoutErrorǁ_default_code'


# 🏗️⚡️⚙️🪄


# <3 🧱🤝🐛🪄
