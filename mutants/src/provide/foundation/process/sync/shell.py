# provide/foundation/process/sync/shell.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from provide.foundation.errors.config import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import DEFAULT_SHELL_ALLOW_FEATURES
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.sync.execution import run
from provide.foundation.process.validation import validate_shell_safety

"""Shell command execution wrapper."""

log = get_logger(__name__)
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


def x_shell__mutmut_orig(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_1(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = False,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_2(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = False,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_3(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_4(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            None,
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_5(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code=None,
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_6(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type=None,
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_7(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=None,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_8(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_9(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_10(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_11(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_12(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "XXShell command must be a stringXX",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_13(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_14(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "SHELL COMMAND MUST BE A STRING",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_15(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="XXINVALID_SHELL_COMMANDXX",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_16(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="invalid_shell_command",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_17(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="XXstrXX",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_18(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="STR",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_19(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(None).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_20(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(None, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_21(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=None)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_22(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_23(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, )

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_24(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        None,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_25(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=None,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_26(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=None,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_27(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=None,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_28(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=None,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_29(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=None,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_30(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=None,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_31(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_32(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_33(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_34(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_35(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_36(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


def x_shell__mutmut_37(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        **kwargs,
    )


def x_shell__mutmut_38(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        )


def x_shell__mutmut_39(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=False,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )

x_shell__mutmut_mutants : ClassVar[MutantDict] = {
'x_shell__mutmut_1': x_shell__mutmut_1, 
    'x_shell__mutmut_2': x_shell__mutmut_2, 
    'x_shell__mutmut_3': x_shell__mutmut_3, 
    'x_shell__mutmut_4': x_shell__mutmut_4, 
    'x_shell__mutmut_5': x_shell__mutmut_5, 
    'x_shell__mutmut_6': x_shell__mutmut_6, 
    'x_shell__mutmut_7': x_shell__mutmut_7, 
    'x_shell__mutmut_8': x_shell__mutmut_8, 
    'x_shell__mutmut_9': x_shell__mutmut_9, 
    'x_shell__mutmut_10': x_shell__mutmut_10, 
    'x_shell__mutmut_11': x_shell__mutmut_11, 
    'x_shell__mutmut_12': x_shell__mutmut_12, 
    'x_shell__mutmut_13': x_shell__mutmut_13, 
    'x_shell__mutmut_14': x_shell__mutmut_14, 
    'x_shell__mutmut_15': x_shell__mutmut_15, 
    'x_shell__mutmut_16': x_shell__mutmut_16, 
    'x_shell__mutmut_17': x_shell__mutmut_17, 
    'x_shell__mutmut_18': x_shell__mutmut_18, 
    'x_shell__mutmut_19': x_shell__mutmut_19, 
    'x_shell__mutmut_20': x_shell__mutmut_20, 
    'x_shell__mutmut_21': x_shell__mutmut_21, 
    'x_shell__mutmut_22': x_shell__mutmut_22, 
    'x_shell__mutmut_23': x_shell__mutmut_23, 
    'x_shell__mutmut_24': x_shell__mutmut_24, 
    'x_shell__mutmut_25': x_shell__mutmut_25, 
    'x_shell__mutmut_26': x_shell__mutmut_26, 
    'x_shell__mutmut_27': x_shell__mutmut_27, 
    'x_shell__mutmut_28': x_shell__mutmut_28, 
    'x_shell__mutmut_29': x_shell__mutmut_29, 
    'x_shell__mutmut_30': x_shell__mutmut_30, 
    'x_shell__mutmut_31': x_shell__mutmut_31, 
    'x_shell__mutmut_32': x_shell__mutmut_32, 
    'x_shell__mutmut_33': x_shell__mutmut_33, 
    'x_shell__mutmut_34': x_shell__mutmut_34, 
    'x_shell__mutmut_35': x_shell__mutmut_35, 
    'x_shell__mutmut_36': x_shell__mutmut_36, 
    'x_shell__mutmut_37': x_shell__mutmut_37, 
    'x_shell__mutmut_38': x_shell__mutmut_38, 
    'x_shell__mutmut_39': x_shell__mutmut_39
}

def shell(*args, **kwargs):
    result = _mutmut_trampoline(x_shell__mutmut_orig, x_shell__mutmut_mutants, args, kwargs)
    return result 

shell.__signature__ = _mutmut_signature(x_shell__mutmut_orig)
x_shell__mutmut_orig.__name__ = 'x_shell'


# <3 🧱🤝🏃🪄
