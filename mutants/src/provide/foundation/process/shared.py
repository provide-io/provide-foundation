# provide/foundation/process/shared.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from attrs import define

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.process import ProcessError

"""Shared utilities for both sync and async subprocess execution."""
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


@define(slots=True)
class CompletedProcess:
    """Result of a completed process.

    Note:
        The `env` field only stores caller-provided environment variable overrides,
        not the full subprocess environment. This prevents credential leakage when
        CompletedProcess objects are logged or stored.
    """

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    cwd: str | None = None
    env: dict[str, str] | None = None  # Only caller overrides, not full environment


def x_prepare_environment__mutmut_orig(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(caller_overrides=env, scrub=True)


def x_prepare_environment__mutmut_1(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(caller_overrides=None, scrub=True)


def x_prepare_environment__mutmut_2(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(caller_overrides=env, scrub=None)


def x_prepare_environment__mutmut_3(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(scrub=True)


def x_prepare_environment__mutmut_4(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(
        caller_overrides=env,
    )


def x_prepare_environment__mutmut_5(env: Mapping[str, str] | None) -> dict[str, str]:
    """Prepare environment for subprocess execution with security scrubbing.

    This function uses environment scrubbing by default to prevent credential
    leakage. Only allowlisted safe variables plus caller overrides are included.

    Args:
        env: Optional environment variables provided by caller (always included)

    Returns:
        Scrubbed environment dictionary for subprocess

    Security Note:
        - System environment is scrubbed to allowlist only
        - Caller overrides (env parameter) are always included
        - Sensitive credentials in os.environ are excluded
        - Result contains <50 vars instead of 100+ from os.environ

    """
    from provide.foundation.process.env import prepare_subprocess_environment

    return prepare_subprocess_environment(caller_overrides=env, scrub=False)


x_prepare_environment__mutmut_mutants: ClassVar[MutantDict] = {
    "x_prepare_environment__mutmut_1": x_prepare_environment__mutmut_1,
    "x_prepare_environment__mutmut_2": x_prepare_environment__mutmut_2,
    "x_prepare_environment__mutmut_3": x_prepare_environment__mutmut_3,
    "x_prepare_environment__mutmut_4": x_prepare_environment__mutmut_4,
    "x_prepare_environment__mutmut_5": x_prepare_environment__mutmut_5,
}


def prepare_environment(*args, **kwargs):
    result = _mutmut_trampoline(
        x_prepare_environment__mutmut_orig, x_prepare_environment__mutmut_mutants, args, kwargs
    )
    return result


prepare_environment.__signature__ = _mutmut_signature(x_prepare_environment__mutmut_orig)
x_prepare_environment__mutmut_orig.__name__ = "x_prepare_environment"


def x_create_completed_process__mutmut_orig(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_1(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = None
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_2(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=None,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_3(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=None,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_4(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=None,
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_5(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=None,
    )


def x_create_completed_process__mutmut_6(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_7(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_8(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_9(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_10(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode(None, errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_11(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors=None),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_12(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode(errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_13(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode(
            "utf-8",
        ),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_14(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("XXutf-8XX", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_15(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("UTF-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_16(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="XXreplaceXX"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_17(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="REPLACE"),
        stderr=stderr.decode("utf-8", errors="replace"),
    )


def x_create_completed_process__mutmut_18(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode(None, errors="replace"),
    )


def x_create_completed_process__mutmut_19(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors=None),
    )


def x_create_completed_process__mutmut_20(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode(errors="replace"),
    )


def x_create_completed_process__mutmut_21(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode(
            "utf-8",
        ),
    )


def x_create_completed_process__mutmut_22(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("XXutf-8XX", errors="replace"),
    )


def x_create_completed_process__mutmut_23(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("UTF-8", errors="replace"),
    )


def x_create_completed_process__mutmut_24(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="XXreplaceXX"),
    )


def x_create_completed_process__mutmut_25(
    cmd: list[str] | str,
    returncode: int,
    stdout: bytes,
    stderr: bytes,
) -> CompletedProcess:
    """Create a CompletedProcess result.

    Args:
        cmd: Command that was executed
        returncode: Process exit code
        stdout: Standard output bytes
        stderr: Standard error bytes

    Returns:
        CompletedProcess with decoded output
    """
    # Ensure args is always a list for CompletedProcess
    args = cmd if isinstance(cmd, list) else [cmd]
    return CompletedProcess(
        args=args,
        returncode=returncode,
        stdout=stdout.decode("utf-8", errors="replace"),
        stderr=stderr.decode("utf-8", errors="REPLACE"),
    )


x_create_completed_process__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_completed_process__mutmut_1": x_create_completed_process__mutmut_1,
    "x_create_completed_process__mutmut_2": x_create_completed_process__mutmut_2,
    "x_create_completed_process__mutmut_3": x_create_completed_process__mutmut_3,
    "x_create_completed_process__mutmut_4": x_create_completed_process__mutmut_4,
    "x_create_completed_process__mutmut_5": x_create_completed_process__mutmut_5,
    "x_create_completed_process__mutmut_6": x_create_completed_process__mutmut_6,
    "x_create_completed_process__mutmut_7": x_create_completed_process__mutmut_7,
    "x_create_completed_process__mutmut_8": x_create_completed_process__mutmut_8,
    "x_create_completed_process__mutmut_9": x_create_completed_process__mutmut_9,
    "x_create_completed_process__mutmut_10": x_create_completed_process__mutmut_10,
    "x_create_completed_process__mutmut_11": x_create_completed_process__mutmut_11,
    "x_create_completed_process__mutmut_12": x_create_completed_process__mutmut_12,
    "x_create_completed_process__mutmut_13": x_create_completed_process__mutmut_13,
    "x_create_completed_process__mutmut_14": x_create_completed_process__mutmut_14,
    "x_create_completed_process__mutmut_15": x_create_completed_process__mutmut_15,
    "x_create_completed_process__mutmut_16": x_create_completed_process__mutmut_16,
    "x_create_completed_process__mutmut_17": x_create_completed_process__mutmut_17,
    "x_create_completed_process__mutmut_18": x_create_completed_process__mutmut_18,
    "x_create_completed_process__mutmut_19": x_create_completed_process__mutmut_19,
    "x_create_completed_process__mutmut_20": x_create_completed_process__mutmut_20,
    "x_create_completed_process__mutmut_21": x_create_completed_process__mutmut_21,
    "x_create_completed_process__mutmut_22": x_create_completed_process__mutmut_22,
    "x_create_completed_process__mutmut_23": x_create_completed_process__mutmut_23,
    "x_create_completed_process__mutmut_24": x_create_completed_process__mutmut_24,
    "x_create_completed_process__mutmut_25": x_create_completed_process__mutmut_25,
}


def create_completed_process(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_completed_process__mutmut_orig, x_create_completed_process__mutmut_mutants, args, kwargs
    )
    return result


create_completed_process.__signature__ = _mutmut_signature(x_create_completed_process__mutmut_orig)
x_create_completed_process__mutmut_orig.__name__ = "x_create_completed_process"


def x_check_process_success__mutmut_orig(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_1(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check or process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_2(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode == 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_3(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 1:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_4(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            None,
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_5(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code=None,
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_6(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=None,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_7(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=None,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_8(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=None,
            command=cmd_str,
        )


def x_check_process_success__mutmut_9(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=None,
        )


def x_check_process_success__mutmut_10(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_11(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_12(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_13(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_14(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            command=cmd_str,
        )


def x_check_process_success__mutmut_15(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
        )


def x_check_process_success__mutmut_16(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="XXCOMMAND_FAILEDXX",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


def x_check_process_success__mutmut_17(
    process_returncode: int,
    cmd_str: str,
    stdout: str,
    stderr: str,
    check: bool,
) -> None:
    """Check if process completed successfully.

    Args:
        process_returncode: Process exit code
        cmd_str: Command string for error messages
        stdout: Standard output
        stderr: Standard error
        check: Whether to raise exception on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process_returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process_returncode}: {cmd_str}",
            code="command_failed",
            exit_code=process_returncode,
            stdout=stdout,
            stderr=stderr,
            command=cmd_str,
        )


x_check_process_success__mutmut_mutants: ClassVar[MutantDict] = {
    "x_check_process_success__mutmut_1": x_check_process_success__mutmut_1,
    "x_check_process_success__mutmut_2": x_check_process_success__mutmut_2,
    "x_check_process_success__mutmut_3": x_check_process_success__mutmut_3,
    "x_check_process_success__mutmut_4": x_check_process_success__mutmut_4,
    "x_check_process_success__mutmut_5": x_check_process_success__mutmut_5,
    "x_check_process_success__mutmut_6": x_check_process_success__mutmut_6,
    "x_check_process_success__mutmut_7": x_check_process_success__mutmut_7,
    "x_check_process_success__mutmut_8": x_check_process_success__mutmut_8,
    "x_check_process_success__mutmut_9": x_check_process_success__mutmut_9,
    "x_check_process_success__mutmut_10": x_check_process_success__mutmut_10,
    "x_check_process_success__mutmut_11": x_check_process_success__mutmut_11,
    "x_check_process_success__mutmut_12": x_check_process_success__mutmut_12,
    "x_check_process_success__mutmut_13": x_check_process_success__mutmut_13,
    "x_check_process_success__mutmut_14": x_check_process_success__mutmut_14,
    "x_check_process_success__mutmut_15": x_check_process_success__mutmut_15,
    "x_check_process_success__mutmut_16": x_check_process_success__mutmut_16,
    "x_check_process_success__mutmut_17": x_check_process_success__mutmut_17,
}


def check_process_success(*args, **kwargs):
    result = _mutmut_trampoline(
        x_check_process_success__mutmut_orig, x_check_process_success__mutmut_mutants, args, kwargs
    )
    return result


check_process_success.__signature__ = _mutmut_signature(x_check_process_success__mutmut_orig)
x_check_process_success__mutmut_orig.__name__ = "x_check_process_success"


def x_check_process_exit_code__mutmut_orig(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_1(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode == 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_2(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 1:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_3(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            None,
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_4(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code=None,
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_5(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=None,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_6(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=None,
        )


def x_check_process_exit_code__mutmut_7(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            code="COMMAND_FAILED",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_8(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_9(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_10(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="COMMAND_FAILED",
            exit_code=process.returncode,
        )


def x_check_process_exit_code__mutmut_11(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="XXCOMMAND_FAILEDXX",
            exit_code=process.returncode,
            command=cmd_str,
        )


def x_check_process_exit_code__mutmut_12(process: Any, cmd_str: str) -> None:
    """Check process exit code and raise if non-zero.

    Args:
        process: Subprocess instance with returncode attribute
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="command_failed",
            exit_code=process.returncode,
            command=cmd_str,
        )


x_check_process_exit_code__mutmut_mutants: ClassVar[MutantDict] = {
    "x_check_process_exit_code__mutmut_1": x_check_process_exit_code__mutmut_1,
    "x_check_process_exit_code__mutmut_2": x_check_process_exit_code__mutmut_2,
    "x_check_process_exit_code__mutmut_3": x_check_process_exit_code__mutmut_3,
    "x_check_process_exit_code__mutmut_4": x_check_process_exit_code__mutmut_4,
    "x_check_process_exit_code__mutmut_5": x_check_process_exit_code__mutmut_5,
    "x_check_process_exit_code__mutmut_6": x_check_process_exit_code__mutmut_6,
    "x_check_process_exit_code__mutmut_7": x_check_process_exit_code__mutmut_7,
    "x_check_process_exit_code__mutmut_8": x_check_process_exit_code__mutmut_8,
    "x_check_process_exit_code__mutmut_9": x_check_process_exit_code__mutmut_9,
    "x_check_process_exit_code__mutmut_10": x_check_process_exit_code__mutmut_10,
    "x_check_process_exit_code__mutmut_11": x_check_process_exit_code__mutmut_11,
    "x_check_process_exit_code__mutmut_12": x_check_process_exit_code__mutmut_12,
}


def check_process_exit_code(*args, **kwargs):
    result = _mutmut_trampoline(
        x_check_process_exit_code__mutmut_orig, x_check_process_exit_code__mutmut_mutants, args, kwargs
    )
    return result


check_process_exit_code.__signature__ = _mutmut_signature(x_check_process_exit_code__mutmut_orig)
x_check_process_exit_code__mutmut_orig.__name__ = "x_check_process_exit_code"


def x_filter_subprocess_kwargs__mutmut_orig(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_1(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = None
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_2(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "XXstdinXX",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_3(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "STDIN",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_4(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "XXstdoutXX",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_5(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "STDOUT",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_6(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "XXstderrXX",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_7(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "STDERR",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_8(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "XXshellXX",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_9(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "SHELL",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_10(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "XXcwdXX",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_11(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "CWD",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_12(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "XXenvXX",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_13(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "ENV",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_14(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "XXuniversal_newlinesXX",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_15(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "UNIVERSAL_NEWLINES",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_16(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "XXstartupinfoXX",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_17(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "STARTUPINFO",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_18(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "XXcreationflagsXX",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_19(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "CREATIONFLAGS",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_20(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "XXrestore_signalsXX",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_21(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "RESTORE_SIGNALS",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_22(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "XXstart_new_sessionXX",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_23(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "START_NEW_SESSION",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_24(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "XXpass_fdsXX",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_25(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "PASS_FDS",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_26(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "XXencodingXX",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_27(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "ENCODING",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_28(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "XXerrorsXX",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_29(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "ERRORS",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_30(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "XXtextXX",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_31(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "TEXT",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_32(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "XXuserXX",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_33(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "USER",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_34(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "XXgroupXX",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_35(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "GROUP",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_36(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "XXextra_groupsXX",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_37(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "EXTRA_GROUPS",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_38(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "XXumaskXX",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_39(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "UMASK",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_40(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "XXpipesizeXX",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_41(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "PIPESIZE",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_42(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "XXprocess_groupXX",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_43(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "PROCESS_GROUP",
    }
    return {k: v for k, v in kwargs.items() if k in valid_subprocess_kwargs}


def x_filter_subprocess_kwargs__mutmut_44(kwargs: dict) -> dict:
    """Filter kwargs to only include valid subprocess parameters.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        Filtered dictionary with only valid subprocess parameters
    """
    valid_subprocess_kwargs = {
        "stdin",
        "stdout",
        "stderr",
        "shell",
        "cwd",
        "env",
        "universal_newlines",
        "startupinfo",
        "creationflags",
        "restore_signals",
        "start_new_session",
        "pass_fds",
        "encoding",
        "errors",
        "text",
        "user",
        "group",
        "extra_groups",
        "umask",
        "pipesize",
        "process_group",
    }
    return {k: v for k, v in kwargs.items() if k not in valid_subprocess_kwargs}


x_filter_subprocess_kwargs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_filter_subprocess_kwargs__mutmut_1": x_filter_subprocess_kwargs__mutmut_1,
    "x_filter_subprocess_kwargs__mutmut_2": x_filter_subprocess_kwargs__mutmut_2,
    "x_filter_subprocess_kwargs__mutmut_3": x_filter_subprocess_kwargs__mutmut_3,
    "x_filter_subprocess_kwargs__mutmut_4": x_filter_subprocess_kwargs__mutmut_4,
    "x_filter_subprocess_kwargs__mutmut_5": x_filter_subprocess_kwargs__mutmut_5,
    "x_filter_subprocess_kwargs__mutmut_6": x_filter_subprocess_kwargs__mutmut_6,
    "x_filter_subprocess_kwargs__mutmut_7": x_filter_subprocess_kwargs__mutmut_7,
    "x_filter_subprocess_kwargs__mutmut_8": x_filter_subprocess_kwargs__mutmut_8,
    "x_filter_subprocess_kwargs__mutmut_9": x_filter_subprocess_kwargs__mutmut_9,
    "x_filter_subprocess_kwargs__mutmut_10": x_filter_subprocess_kwargs__mutmut_10,
    "x_filter_subprocess_kwargs__mutmut_11": x_filter_subprocess_kwargs__mutmut_11,
    "x_filter_subprocess_kwargs__mutmut_12": x_filter_subprocess_kwargs__mutmut_12,
    "x_filter_subprocess_kwargs__mutmut_13": x_filter_subprocess_kwargs__mutmut_13,
    "x_filter_subprocess_kwargs__mutmut_14": x_filter_subprocess_kwargs__mutmut_14,
    "x_filter_subprocess_kwargs__mutmut_15": x_filter_subprocess_kwargs__mutmut_15,
    "x_filter_subprocess_kwargs__mutmut_16": x_filter_subprocess_kwargs__mutmut_16,
    "x_filter_subprocess_kwargs__mutmut_17": x_filter_subprocess_kwargs__mutmut_17,
    "x_filter_subprocess_kwargs__mutmut_18": x_filter_subprocess_kwargs__mutmut_18,
    "x_filter_subprocess_kwargs__mutmut_19": x_filter_subprocess_kwargs__mutmut_19,
    "x_filter_subprocess_kwargs__mutmut_20": x_filter_subprocess_kwargs__mutmut_20,
    "x_filter_subprocess_kwargs__mutmut_21": x_filter_subprocess_kwargs__mutmut_21,
    "x_filter_subprocess_kwargs__mutmut_22": x_filter_subprocess_kwargs__mutmut_22,
    "x_filter_subprocess_kwargs__mutmut_23": x_filter_subprocess_kwargs__mutmut_23,
    "x_filter_subprocess_kwargs__mutmut_24": x_filter_subprocess_kwargs__mutmut_24,
    "x_filter_subprocess_kwargs__mutmut_25": x_filter_subprocess_kwargs__mutmut_25,
    "x_filter_subprocess_kwargs__mutmut_26": x_filter_subprocess_kwargs__mutmut_26,
    "x_filter_subprocess_kwargs__mutmut_27": x_filter_subprocess_kwargs__mutmut_27,
    "x_filter_subprocess_kwargs__mutmut_28": x_filter_subprocess_kwargs__mutmut_28,
    "x_filter_subprocess_kwargs__mutmut_29": x_filter_subprocess_kwargs__mutmut_29,
    "x_filter_subprocess_kwargs__mutmut_30": x_filter_subprocess_kwargs__mutmut_30,
    "x_filter_subprocess_kwargs__mutmut_31": x_filter_subprocess_kwargs__mutmut_31,
    "x_filter_subprocess_kwargs__mutmut_32": x_filter_subprocess_kwargs__mutmut_32,
    "x_filter_subprocess_kwargs__mutmut_33": x_filter_subprocess_kwargs__mutmut_33,
    "x_filter_subprocess_kwargs__mutmut_34": x_filter_subprocess_kwargs__mutmut_34,
    "x_filter_subprocess_kwargs__mutmut_35": x_filter_subprocess_kwargs__mutmut_35,
    "x_filter_subprocess_kwargs__mutmut_36": x_filter_subprocess_kwargs__mutmut_36,
    "x_filter_subprocess_kwargs__mutmut_37": x_filter_subprocess_kwargs__mutmut_37,
    "x_filter_subprocess_kwargs__mutmut_38": x_filter_subprocess_kwargs__mutmut_38,
    "x_filter_subprocess_kwargs__mutmut_39": x_filter_subprocess_kwargs__mutmut_39,
    "x_filter_subprocess_kwargs__mutmut_40": x_filter_subprocess_kwargs__mutmut_40,
    "x_filter_subprocess_kwargs__mutmut_41": x_filter_subprocess_kwargs__mutmut_41,
    "x_filter_subprocess_kwargs__mutmut_42": x_filter_subprocess_kwargs__mutmut_42,
    "x_filter_subprocess_kwargs__mutmut_43": x_filter_subprocess_kwargs__mutmut_43,
    "x_filter_subprocess_kwargs__mutmut_44": x_filter_subprocess_kwargs__mutmut_44,
}


def filter_subprocess_kwargs(*args, **kwargs):
    result = _mutmut_trampoline(
        x_filter_subprocess_kwargs__mutmut_orig, x_filter_subprocess_kwargs__mutmut_mutants, args, kwargs
    )
    return result


filter_subprocess_kwargs.__signature__ = _mutmut_signature(x_filter_subprocess_kwargs__mutmut_orig)
x_filter_subprocess_kwargs__mutmut_orig.__name__ = "x_filter_subprocess_kwargs"


def x_normalize_cwd__mutmut_orig(cwd: str | Path | None) -> str | None:
    """Normalize working directory to string.

    Args:
        cwd: Working directory as string, Path, or None

    Returns:
        Working directory as string or None
    """
    if isinstance(cwd, Path):
        return str(cwd)
    return cwd


def x_normalize_cwd__mutmut_1(cwd: str | Path | None) -> str | None:
    """Normalize working directory to string.

    Args:
        cwd: Working directory as string, Path, or None

    Returns:
        Working directory as string or None
    """
    if isinstance(cwd, Path):
        return str(None)
    return cwd


x_normalize_cwd__mutmut_mutants: ClassVar[MutantDict] = {
    "x_normalize_cwd__mutmut_1": x_normalize_cwd__mutmut_1
}


def normalize_cwd(*args, **kwargs):
    result = _mutmut_trampoline(x_normalize_cwd__mutmut_orig, x_normalize_cwd__mutmut_mutants, args, kwargs)
    return result


normalize_cwd.__signature__ = _mutmut_signature(x_normalize_cwd__mutmut_orig)
x_normalize_cwd__mutmut_orig.__name__ = "x_normalize_cwd"


def x_prepare_input__mutmut_orig(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_1(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is not None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_2(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode or isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_3(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode(None)
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_4(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("XXutf-8XX")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_5(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("UTF-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_6(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode or isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_7(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("utf-8")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_8(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode(None)
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_9(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("XXutf-8XX")
    else:
        # Already correct type
        return input


def x_prepare_input__mutmut_10(input: str | bytes | None, text_mode: bool) -> str | bytes | None:
    """Prepare input for subprocess based on text mode.

    Args:
        input: Input data as string, bytes, or None
        text_mode: Whether subprocess is in text mode

    Returns:
        Properly converted input for subprocess
    """
    if input is None:
        return None

    if text_mode and isinstance(input, bytes):
        # Convert bytes to string for text mode
        return input.decode("utf-8")
    elif not text_mode and isinstance(input, str):
        # Convert string to bytes for binary mode
        return input.encode("UTF-8")
    else:
        # Already correct type
        return input


x_prepare_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x_prepare_input__mutmut_1": x_prepare_input__mutmut_1,
    "x_prepare_input__mutmut_2": x_prepare_input__mutmut_2,
    "x_prepare_input__mutmut_3": x_prepare_input__mutmut_3,
    "x_prepare_input__mutmut_4": x_prepare_input__mutmut_4,
    "x_prepare_input__mutmut_5": x_prepare_input__mutmut_5,
    "x_prepare_input__mutmut_6": x_prepare_input__mutmut_6,
    "x_prepare_input__mutmut_7": x_prepare_input__mutmut_7,
    "x_prepare_input__mutmut_8": x_prepare_input__mutmut_8,
    "x_prepare_input__mutmut_9": x_prepare_input__mutmut_9,
    "x_prepare_input__mutmut_10": x_prepare_input__mutmut_10,
}


def prepare_input(*args, **kwargs):
    result = _mutmut_trampoline(x_prepare_input__mutmut_orig, x_prepare_input__mutmut_mutants, args, kwargs)
    return result


prepare_input.__signature__ = _mutmut_signature(x_prepare_input__mutmut_orig)
x_prepare_input__mutmut_orig.__name__ = "x_prepare_input"


def x_validate_command_type__mutmut_orig(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_1(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) or not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_2(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_3(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            None,
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_4(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code=None,
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_5(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected=None,
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_6(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual=None,
        )


def x_validate_command_type__mutmut_7(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_8(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_9(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_10(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
        )


def x_validate_command_type__mutmut_11(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "XXString commands require explicit shell=True for security. XX"
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_12(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "string commands require explicit shell=true for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_13(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "STRING COMMANDS REQUIRE EXPLICIT SHELL=TRUE FOR SECURITY. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_14(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "XXUse shell() for shell commands or pass a list for direct execution.XX",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_15(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_16(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "USE SHELL() FOR SHELL COMMANDS OR PASS A LIST FOR DIRECT EXECUTION.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_17(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="XXINVALID_COMMAND_TYPEXX",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_18(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="invalid_command_type",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_19(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="XXlist[str] or (str with shell=True)XX",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_20(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=true)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_21(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="LIST[STR] OR (STR WITH SHELL=TRUE)",
            actual="str without shell=True",
        )


def x_validate_command_type__mutmut_22(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="XXstr without shell=TrueXX",
        )


def x_validate_command_type__mutmut_23(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=true",
        )


def x_validate_command_type__mutmut_24(cmd: list[str] | str, shell: bool) -> None:
    """Validate command type matches shell parameter.

    Args:
        cmd: Command as list or string
        shell: Whether shell execution is enabled

    Raises:
        ValidationError: If string command provided without shell=True
    """
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="STR WITHOUT SHELL=TRUE",
        )


x_validate_command_type__mutmut_mutants: ClassVar[MutantDict] = {
    "x_validate_command_type__mutmut_1": x_validate_command_type__mutmut_1,
    "x_validate_command_type__mutmut_2": x_validate_command_type__mutmut_2,
    "x_validate_command_type__mutmut_3": x_validate_command_type__mutmut_3,
    "x_validate_command_type__mutmut_4": x_validate_command_type__mutmut_4,
    "x_validate_command_type__mutmut_5": x_validate_command_type__mutmut_5,
    "x_validate_command_type__mutmut_6": x_validate_command_type__mutmut_6,
    "x_validate_command_type__mutmut_7": x_validate_command_type__mutmut_7,
    "x_validate_command_type__mutmut_8": x_validate_command_type__mutmut_8,
    "x_validate_command_type__mutmut_9": x_validate_command_type__mutmut_9,
    "x_validate_command_type__mutmut_10": x_validate_command_type__mutmut_10,
    "x_validate_command_type__mutmut_11": x_validate_command_type__mutmut_11,
    "x_validate_command_type__mutmut_12": x_validate_command_type__mutmut_12,
    "x_validate_command_type__mutmut_13": x_validate_command_type__mutmut_13,
    "x_validate_command_type__mutmut_14": x_validate_command_type__mutmut_14,
    "x_validate_command_type__mutmut_15": x_validate_command_type__mutmut_15,
    "x_validate_command_type__mutmut_16": x_validate_command_type__mutmut_16,
    "x_validate_command_type__mutmut_17": x_validate_command_type__mutmut_17,
    "x_validate_command_type__mutmut_18": x_validate_command_type__mutmut_18,
    "x_validate_command_type__mutmut_19": x_validate_command_type__mutmut_19,
    "x_validate_command_type__mutmut_20": x_validate_command_type__mutmut_20,
    "x_validate_command_type__mutmut_21": x_validate_command_type__mutmut_21,
    "x_validate_command_type__mutmut_22": x_validate_command_type__mutmut_22,
    "x_validate_command_type__mutmut_23": x_validate_command_type__mutmut_23,
    "x_validate_command_type__mutmut_24": x_validate_command_type__mutmut_24,
}


def validate_command_type(*args, **kwargs):
    result = _mutmut_trampoline(
        x_validate_command_type__mutmut_orig, x_validate_command_type__mutmut_mutants, args, kwargs
    )
    return result


validate_command_type.__signature__ = _mutmut_signature(x_validate_command_type__mutmut_orig)
x_validate_command_type__mutmut_orig.__name__ = "x_validate_command_type"


# <3 🧱🤝🏃🪄
