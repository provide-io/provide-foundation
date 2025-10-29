# provide/foundation/process/lifecycle/monitoring.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio

from provide.foundation.errors.process import ProcessError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import DEFAULT_PROCESS_WAIT_TIMEOUT
from provide.foundation.process.lifecycle.managed import ManagedProcess

"""Process output monitoring utilities.

This module provides async utilities for monitoring and waiting for specific
output patterns from managed processes.
"""

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


def x__drain_remaining_output__mutmut_orig(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_1(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process or process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_2(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = None
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_3(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer = (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_4(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer -= (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_5(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode(None, errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_6(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors=None) if isinstance(remaining, bytes) else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_7(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode(errors="replace") if isinstance(remaining, bytes) else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_8(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode(
                        "utf-8",
                    )
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_9(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("XXutf-8XX", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_10(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("UTF-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_11(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="XXreplaceXX")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_12(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="REPLACE")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_13(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace") if isinstance(remaining, bytes) else str(None)
                )
                log.debug("Read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_14(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug(None, size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_15(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("Read remaining output from exited process", size=None)
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_16(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug(size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_17(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug(
                    "Read remaining output from exited process",
                )
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_18(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("XXRead remaining output from exited processXX", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_19(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("read remaining output from exited process", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


def x__drain_remaining_output__mutmut_20(process: ManagedProcess, buffer: str) -> str:
    """Drain any remaining output from process pipes."""
    if process._process and process._process.stdout:
        try:
            remaining = process._process.stdout.read()
            if remaining:
                buffer += (
                    remaining.decode("utf-8", errors="replace")
                    if isinstance(remaining, bytes)
                    else str(remaining)
                )
                log.debug("READ REMAINING OUTPUT FROM EXITED PROCESS", size=len(remaining))
        except (OSError, ValueError, AttributeError):
            # OSError: stream/file read errors
            # ValueError: invalid stream state or decoding errors
            # AttributeError: stdout/stderr unavailable
            pass
    return buffer


x__drain_remaining_output__mutmut_mutants: ClassVar[MutantDict] = {
    "x__drain_remaining_output__mutmut_1": x__drain_remaining_output__mutmut_1,
    "x__drain_remaining_output__mutmut_2": x__drain_remaining_output__mutmut_2,
    "x__drain_remaining_output__mutmut_3": x__drain_remaining_output__mutmut_3,
    "x__drain_remaining_output__mutmut_4": x__drain_remaining_output__mutmut_4,
    "x__drain_remaining_output__mutmut_5": x__drain_remaining_output__mutmut_5,
    "x__drain_remaining_output__mutmut_6": x__drain_remaining_output__mutmut_6,
    "x__drain_remaining_output__mutmut_7": x__drain_remaining_output__mutmut_7,
    "x__drain_remaining_output__mutmut_8": x__drain_remaining_output__mutmut_8,
    "x__drain_remaining_output__mutmut_9": x__drain_remaining_output__mutmut_9,
    "x__drain_remaining_output__mutmut_10": x__drain_remaining_output__mutmut_10,
    "x__drain_remaining_output__mutmut_11": x__drain_remaining_output__mutmut_11,
    "x__drain_remaining_output__mutmut_12": x__drain_remaining_output__mutmut_12,
    "x__drain_remaining_output__mutmut_13": x__drain_remaining_output__mutmut_13,
    "x__drain_remaining_output__mutmut_14": x__drain_remaining_output__mutmut_14,
    "x__drain_remaining_output__mutmut_15": x__drain_remaining_output__mutmut_15,
    "x__drain_remaining_output__mutmut_16": x__drain_remaining_output__mutmut_16,
    "x__drain_remaining_output__mutmut_17": x__drain_remaining_output__mutmut_17,
    "x__drain_remaining_output__mutmut_18": x__drain_remaining_output__mutmut_18,
    "x__drain_remaining_output__mutmut_19": x__drain_remaining_output__mutmut_19,
    "x__drain_remaining_output__mutmut_20": x__drain_remaining_output__mutmut_20,
}


def _drain_remaining_output(*args, **kwargs):
    result = _mutmut_trampoline(
        x__drain_remaining_output__mutmut_orig, x__drain_remaining_output__mutmut_mutants, args, kwargs
    )
    return result


_drain_remaining_output.__signature__ = _mutmut_signature(x__drain_remaining_output__mutmut_orig)
x__drain_remaining_output__mutmut_orig.__name__ = "x__drain_remaining_output"


def x__check_pattern_found__mutmut_orig(buffer: str, expected_parts: list[str]) -> bool:
    """Check if all expected parts are found in buffer."""
    return all(part in buffer for part in expected_parts)


def x__check_pattern_found__mutmut_1(buffer: str, expected_parts: list[str]) -> bool:
    """Check if all expected parts are found in buffer."""
    return all(None)


def x__check_pattern_found__mutmut_2(buffer: str, expected_parts: list[str]) -> bool:
    """Check if all expected parts are found in buffer."""
    return all(part not in buffer for part in expected_parts)


x__check_pattern_found__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_pattern_found__mutmut_1": x__check_pattern_found__mutmut_1,
    "x__check_pattern_found__mutmut_2": x__check_pattern_found__mutmut_2,
}


def _check_pattern_found(*args, **kwargs):
    result = _mutmut_trampoline(
        x__check_pattern_found__mutmut_orig, x__check_pattern_found__mutmut_mutants, args, kwargs
    )
    return result


_check_pattern_found.__signature__ = _mutmut_signature(x__check_pattern_found__mutmut_orig)
x__check_pattern_found__mutmut_orig.__name__ = "x__check_pattern_found"


def x__handle_process_error_exit__mutmut_orig(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_1(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error(None, returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_2(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=None, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_3(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=exit_code, buffer=None)
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_4(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error(returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_5(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_6(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error(
        "Process exited with error",
        returncode=exit_code,
    )
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_7(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("XXProcess exited with errorXX", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_8(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("process exited with error", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_9(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("PROCESS EXITED WITH ERROR", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_10(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=exit_code, buffer=buffer[:201])
    raise ProcessError(f"Process exited with code {exit_code}")


def x__handle_process_error_exit__mutmut_11(exit_code: int, buffer: str) -> None:
    """Handle process exit with error code."""
    log.error("Process exited with error", returncode=exit_code, buffer=buffer[:200])
    raise ProcessError(None)


x__handle_process_error_exit__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_process_error_exit__mutmut_1": x__handle_process_error_exit__mutmut_1,
    "x__handle_process_error_exit__mutmut_2": x__handle_process_error_exit__mutmut_2,
    "x__handle_process_error_exit__mutmut_3": x__handle_process_error_exit__mutmut_3,
    "x__handle_process_error_exit__mutmut_4": x__handle_process_error_exit__mutmut_4,
    "x__handle_process_error_exit__mutmut_5": x__handle_process_error_exit__mutmut_5,
    "x__handle_process_error_exit__mutmut_6": x__handle_process_error_exit__mutmut_6,
    "x__handle_process_error_exit__mutmut_7": x__handle_process_error_exit__mutmut_7,
    "x__handle_process_error_exit__mutmut_8": x__handle_process_error_exit__mutmut_8,
    "x__handle_process_error_exit__mutmut_9": x__handle_process_error_exit__mutmut_9,
    "x__handle_process_error_exit__mutmut_10": x__handle_process_error_exit__mutmut_10,
    "x__handle_process_error_exit__mutmut_11": x__handle_process_error_exit__mutmut_11,
}


def _handle_process_error_exit(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_process_error_exit__mutmut_orig, x__handle_process_error_exit__mutmut_mutants, args, kwargs
    )
    return result


_handle_process_error_exit.__signature__ = _mutmut_signature(x__handle_process_error_exit__mutmut_orig)
x__handle_process_error_exit__mutmut_orig.__name__ = "x__handle_process_error_exit"


def x__handle_process_clean_exit_without_pattern__mutmut_orig(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_1(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error(None, returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_2(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=None, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_3(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=0, buffer=None)
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_4(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error(returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_5(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_6(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error(
        "Process exited without expected output",
        returncode=0,
    )
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_7(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("XXProcess exited without expected outputXX", returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_8(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("process exited without expected output", returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_9(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("PROCESS EXITED WITHOUT EXPECTED OUTPUT", returncode=0, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_10(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=1, buffer=buffer[:200])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_11(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=0, buffer=buffer[:201])
    raise ProcessError(f"Process exited with code {exit_code} before expected output found")


def x__handle_process_clean_exit_without_pattern__mutmut_12(exit_code: int | None, buffer: str) -> None:
    """Handle process clean exit but expected pattern not found."""
    log.error("Process exited without expected output", returncode=0, buffer=buffer[:200])
    raise ProcessError(None)


x__handle_process_clean_exit_without_pattern__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_process_clean_exit_without_pattern__mutmut_1": x__handle_process_clean_exit_without_pattern__mutmut_1,
    "x__handle_process_clean_exit_without_pattern__mutmut_2": x__handle_process_clean_exit_without_pattern__mutmut_2,
    "x__handle_process_clean_exit_without_pattern__mutmut_3": x__handle_process_clean_exit_without_pattern__mutmut_3,
    "x__handle_process_clean_exit_without_pattern__mutmut_4": x__handle_process_clean_exit_without_pattern__mutmut_4,
    "x__handle_process_clean_exit_without_pattern__mutmut_5": x__handle_process_clean_exit_without_pattern__mutmut_5,
    "x__handle_process_clean_exit_without_pattern__mutmut_6": x__handle_process_clean_exit_without_pattern__mutmut_6,
    "x__handle_process_clean_exit_without_pattern__mutmut_7": x__handle_process_clean_exit_without_pattern__mutmut_7,
    "x__handle_process_clean_exit_without_pattern__mutmut_8": x__handle_process_clean_exit_without_pattern__mutmut_8,
    "x__handle_process_clean_exit_without_pattern__mutmut_9": x__handle_process_clean_exit_without_pattern__mutmut_9,
    "x__handle_process_clean_exit_without_pattern__mutmut_10": x__handle_process_clean_exit_without_pattern__mutmut_10,
    "x__handle_process_clean_exit_without_pattern__mutmut_11": x__handle_process_clean_exit_without_pattern__mutmut_11,
    "x__handle_process_clean_exit_without_pattern__mutmut_12": x__handle_process_clean_exit_without_pattern__mutmut_12,
}


def _handle_process_clean_exit_without_pattern(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_process_clean_exit_without_pattern__mutmut_orig,
        x__handle_process_clean_exit_without_pattern__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_handle_process_clean_exit_without_pattern.__signature__ = _mutmut_signature(
    x__handle_process_clean_exit_without_pattern__mutmut_orig
)
x__handle_process_clean_exit_without_pattern__mutmut_orig.__name__ = (
    "x__handle_process_clean_exit_without_pattern"
)


async def x__handle_exited_process__mutmut_orig(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_1(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = None

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_2(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(None, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_3(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, None)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_4(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_5(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(
        process,
    )

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_6(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(None, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_7(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, None):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_8(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_9(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(
        buffer,
    ):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_10(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug(None)
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_11(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("XXFound expected pattern after process exitXX")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_12(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_13(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("FOUND EXPECTED PATTERN AFTER PROCESS EXIT")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_14(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_15(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code == 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_16(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 1:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_17(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(None, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_18(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, None)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_19(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_20(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(
                last_exit_code,
            )

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_21(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(None)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_22(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(1.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_23(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = None

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_24(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(None, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_25(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, None)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_26(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_27(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(
            process,
        )

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_28(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(None, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_29(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, None):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_30(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_31(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(
            buffer,
        ):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_32(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug(None)
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_33(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("XXFound expected pattern after final drainXX")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_34(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_35(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("FOUND EXPECTED PATTERN AFTER FINAL DRAIN")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_36(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(None, buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_37(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(last_exit_code, None)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_38(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(buffer)

    return buffer  # Should never reach here due to exceptions above


async def x__handle_exited_process__mutmut_39(
    process: ManagedProcess,
    buffer: str,
    expected_parts: list[str],
    last_exit_code: int | None,
) -> str:
    """Handle a process that has exited - drain output and check for pattern."""
    # Try to drain any remaining output from the pipes
    buffer = _drain_remaining_output(process, buffer)

    # Check buffer after draining
    if _check_pattern_found(buffer, expected_parts):
        log.debug("Found expected pattern after process exit")
        return buffer

    # If process exited and we don't have the pattern, handle error cases
    if last_exit_code is not None:
        if last_exit_code != 0:
            _handle_process_error_exit(last_exit_code, buffer)

        # For exit code 0, give it a small window to collect buffered output
        await asyncio.sleep(0.1)
        # Try one more time to drain output
        buffer = _drain_remaining_output(process, buffer)

        # Final check
        if _check_pattern_found(buffer, expected_parts):
            log.debug("Found expected pattern after final drain")
            return buffer

        # Process exited cleanly but pattern not found
        _handle_process_clean_exit_without_pattern(
            last_exit_code,
        )

    return buffer  # Should never reach here due to exceptions above


x__handle_exited_process__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_exited_process__mutmut_1": x__handle_exited_process__mutmut_1,
    "x__handle_exited_process__mutmut_2": x__handle_exited_process__mutmut_2,
    "x__handle_exited_process__mutmut_3": x__handle_exited_process__mutmut_3,
    "x__handle_exited_process__mutmut_4": x__handle_exited_process__mutmut_4,
    "x__handle_exited_process__mutmut_5": x__handle_exited_process__mutmut_5,
    "x__handle_exited_process__mutmut_6": x__handle_exited_process__mutmut_6,
    "x__handle_exited_process__mutmut_7": x__handle_exited_process__mutmut_7,
    "x__handle_exited_process__mutmut_8": x__handle_exited_process__mutmut_8,
    "x__handle_exited_process__mutmut_9": x__handle_exited_process__mutmut_9,
    "x__handle_exited_process__mutmut_10": x__handle_exited_process__mutmut_10,
    "x__handle_exited_process__mutmut_11": x__handle_exited_process__mutmut_11,
    "x__handle_exited_process__mutmut_12": x__handle_exited_process__mutmut_12,
    "x__handle_exited_process__mutmut_13": x__handle_exited_process__mutmut_13,
    "x__handle_exited_process__mutmut_14": x__handle_exited_process__mutmut_14,
    "x__handle_exited_process__mutmut_15": x__handle_exited_process__mutmut_15,
    "x__handle_exited_process__mutmut_16": x__handle_exited_process__mutmut_16,
    "x__handle_exited_process__mutmut_17": x__handle_exited_process__mutmut_17,
    "x__handle_exited_process__mutmut_18": x__handle_exited_process__mutmut_18,
    "x__handle_exited_process__mutmut_19": x__handle_exited_process__mutmut_19,
    "x__handle_exited_process__mutmut_20": x__handle_exited_process__mutmut_20,
    "x__handle_exited_process__mutmut_21": x__handle_exited_process__mutmut_21,
    "x__handle_exited_process__mutmut_22": x__handle_exited_process__mutmut_22,
    "x__handle_exited_process__mutmut_23": x__handle_exited_process__mutmut_23,
    "x__handle_exited_process__mutmut_24": x__handle_exited_process__mutmut_24,
    "x__handle_exited_process__mutmut_25": x__handle_exited_process__mutmut_25,
    "x__handle_exited_process__mutmut_26": x__handle_exited_process__mutmut_26,
    "x__handle_exited_process__mutmut_27": x__handle_exited_process__mutmut_27,
    "x__handle_exited_process__mutmut_28": x__handle_exited_process__mutmut_28,
    "x__handle_exited_process__mutmut_29": x__handle_exited_process__mutmut_29,
    "x__handle_exited_process__mutmut_30": x__handle_exited_process__mutmut_30,
    "x__handle_exited_process__mutmut_31": x__handle_exited_process__mutmut_31,
    "x__handle_exited_process__mutmut_32": x__handle_exited_process__mutmut_32,
    "x__handle_exited_process__mutmut_33": x__handle_exited_process__mutmut_33,
    "x__handle_exited_process__mutmut_34": x__handle_exited_process__mutmut_34,
    "x__handle_exited_process__mutmut_35": x__handle_exited_process__mutmut_35,
    "x__handle_exited_process__mutmut_36": x__handle_exited_process__mutmut_36,
    "x__handle_exited_process__mutmut_37": x__handle_exited_process__mutmut_37,
    "x__handle_exited_process__mutmut_38": x__handle_exited_process__mutmut_38,
    "x__handle_exited_process__mutmut_39": x__handle_exited_process__mutmut_39,
}


def _handle_exited_process(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_exited_process__mutmut_orig, x__handle_exited_process__mutmut_mutants, args, kwargs
    )
    return result


_handle_exited_process.__signature__ = _mutmut_signature(x__handle_exited_process__mutmut_orig)
x__handle_exited_process__mutmut_orig.__name__ = "x__handle_exited_process"


async def x__try_read_process_line__mutmut_orig(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_1(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = None
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_2(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=None)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_3(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=1.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_4(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer = line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_5(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer -= line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_6(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line - "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_7(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "XX\nXX"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_8(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug(None, line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_9(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=None)

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_10(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug(line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_11(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug(
                "Read line from process",
            )

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_12(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("XXRead line from processXX", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_13(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_14(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("READ LINE FROM PROCESS", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_15(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:101])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_16(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(None, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_17(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, None):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_18(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_19(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(
                buffer,
            ):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_20(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug(None)
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_21(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("XXFound expected pattern in bufferXX")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_22(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_23(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("FOUND EXPECTED PATTERN IN BUFFER")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_24(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, False

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, False


async def x__try_read_process_line__mutmut_25(
    process: ManagedProcess, buffer: str, expected_parts: list[str]
) -> tuple[str, bool]:
    """Try to read a line from process. Returns (new_buffer, pattern_found)."""
    try:
        # Try to read a line with short timeout
        line = await process.read_line_async(timeout=0.1)
        if line:
            buffer += line + "\n"  # Add newline back since readline strips it
            log.debug("Read line from process", line=line[:100])

            # Check if we have all expected parts
            if _check_pattern_found(buffer, expected_parts):
                log.debug("Found expected pattern in buffer")
                return buffer, True

    except TimeoutError:
        pass
    except (ProcessLookupError, PermissionError, OSError):
        # ProcessLookupError: process already exited
        # PermissionError: process inaccessible
        # OSError: process stream/state errors
        pass

    return buffer, True


x__try_read_process_line__mutmut_mutants: ClassVar[MutantDict] = {
    "x__try_read_process_line__mutmut_1": x__try_read_process_line__mutmut_1,
    "x__try_read_process_line__mutmut_2": x__try_read_process_line__mutmut_2,
    "x__try_read_process_line__mutmut_3": x__try_read_process_line__mutmut_3,
    "x__try_read_process_line__mutmut_4": x__try_read_process_line__mutmut_4,
    "x__try_read_process_line__mutmut_5": x__try_read_process_line__mutmut_5,
    "x__try_read_process_line__mutmut_6": x__try_read_process_line__mutmut_6,
    "x__try_read_process_line__mutmut_7": x__try_read_process_line__mutmut_7,
    "x__try_read_process_line__mutmut_8": x__try_read_process_line__mutmut_8,
    "x__try_read_process_line__mutmut_9": x__try_read_process_line__mutmut_9,
    "x__try_read_process_line__mutmut_10": x__try_read_process_line__mutmut_10,
    "x__try_read_process_line__mutmut_11": x__try_read_process_line__mutmut_11,
    "x__try_read_process_line__mutmut_12": x__try_read_process_line__mutmut_12,
    "x__try_read_process_line__mutmut_13": x__try_read_process_line__mutmut_13,
    "x__try_read_process_line__mutmut_14": x__try_read_process_line__mutmut_14,
    "x__try_read_process_line__mutmut_15": x__try_read_process_line__mutmut_15,
    "x__try_read_process_line__mutmut_16": x__try_read_process_line__mutmut_16,
    "x__try_read_process_line__mutmut_17": x__try_read_process_line__mutmut_17,
    "x__try_read_process_line__mutmut_18": x__try_read_process_line__mutmut_18,
    "x__try_read_process_line__mutmut_19": x__try_read_process_line__mutmut_19,
    "x__try_read_process_line__mutmut_20": x__try_read_process_line__mutmut_20,
    "x__try_read_process_line__mutmut_21": x__try_read_process_line__mutmut_21,
    "x__try_read_process_line__mutmut_22": x__try_read_process_line__mutmut_22,
    "x__try_read_process_line__mutmut_23": x__try_read_process_line__mutmut_23,
    "x__try_read_process_line__mutmut_24": x__try_read_process_line__mutmut_24,
    "x__try_read_process_line__mutmut_25": x__try_read_process_line__mutmut_25,
}


def _try_read_process_line(*args, **kwargs):
    result = _mutmut_trampoline(
        x__try_read_process_line__mutmut_orig, x__try_read_process_line__mutmut_mutants, args, kwargs
    )
    return result


_try_read_process_line.__signature__ = _mutmut_signature(x__try_read_process_line__mutmut_orig)
x__try_read_process_line__mutmut_orig.__name__ = "x__try_read_process_line"


async def x_wait_for_process_output__mutmut_orig(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_1(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1025,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_2(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = None
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_3(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = None
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_4(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = None
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_5(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = "XXXX"
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_6(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = ""

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_7(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        None,
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_8(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=None,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_9(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=None,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_10(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_11(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_12(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_13(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "XX⏳ Waiting for process output patternXX",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_14(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_15(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ WAITING FOR PROCESS OUTPUT PATTERN",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_16(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() + start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_17(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) <= timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_18(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_19(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = None
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_20(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug(None, returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_21(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=None)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_22(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug(returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_23(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug(
                "Process exited",
            )
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_24(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("XXProcess exitedXX", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_25(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_26(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("PROCESS EXITED", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_27(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(None, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_28(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, None, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_29(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, None, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_30(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, None)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_31(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_32(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_33(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_34(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(
                process,
                buffer,
                expected_parts,
            )

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_35(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = None
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_36(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(None, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_37(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, None, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_38(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, None)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_39(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_40(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_41(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(
            process,
            buffer,
        )
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_42(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(None)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_43(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(1.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_44(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(None, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_45(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, None):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_46(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_47(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(
        buffer,
    ):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_48(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        None,
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_49(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=None,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_50(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=None,
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_51(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=None,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_52(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_53(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_54(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_55(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_56(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "XXTimeout waiting for patternXX",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_57(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_58(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "TIMEOUT WAITING FOR PATTERN",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_59(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:201],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(f"Expected pattern {expected_parts} not found within {timeout}s timeout")


async def x_wait_for_process_output__mutmut_60(
    process: ManagedProcess,
    expected_parts: list[str],
    timeout: float = DEFAULT_PROCESS_WAIT_TIMEOUT,
    buffer_size: int = 1024,
) -> str:
    """Wait for specific output pattern from a managed process.

    This utility reads from a process stdout until a specific pattern
    (e.g., handshake string with multiple pipe separators) appears.

    Args:
        process: The managed process to read from
        expected_parts: List of expected parts/separators in the output
        timeout: Maximum time to wait for the pattern
        buffer_size: Size of read buffer

    Returns:
        The complete output buffer containing the expected pattern

    Raises:
        ProcessError: If process exits unexpectedly
        TimeoutError: If pattern is not found within timeout

    """
    loop = asyncio.get_event_loop()
    start_time = loop.time()
    buffer = ""
    last_exit_code = None

    log.debug(
        "⏳ Waiting for process output pattern",
        expected_parts=expected_parts,
        timeout=timeout,
    )

    while (loop.time() - start_time) < timeout:
        # Check if process has exited
        if not process.is_running():
            last_exit_code = process.returncode
            log.debug("Process exited", returncode=last_exit_code)
            return await _handle_exited_process(process, buffer, expected_parts, last_exit_code)

        # Try to read line from running process
        buffer, pattern_found = await _try_read_process_line(process, buffer, expected_parts)
        if pattern_found:
            return buffer

        # Short sleep to avoid busy loop
        await asyncio.sleep(0.01)

    # Final check of buffer before timeout error
    if _check_pattern_found(buffer, expected_parts):
        return buffer

    # If process exited with 0 but we didn't get output, that's still a timeout
    log.error(
        "Timeout waiting for pattern",
        expected_parts=expected_parts,
        buffer=buffer[:200],
        last_exit_code=last_exit_code,
    )
    raise TimeoutError(None)


x_wait_for_process_output__mutmut_mutants: ClassVar[MutantDict] = {
    "x_wait_for_process_output__mutmut_1": x_wait_for_process_output__mutmut_1,
    "x_wait_for_process_output__mutmut_2": x_wait_for_process_output__mutmut_2,
    "x_wait_for_process_output__mutmut_3": x_wait_for_process_output__mutmut_3,
    "x_wait_for_process_output__mutmut_4": x_wait_for_process_output__mutmut_4,
    "x_wait_for_process_output__mutmut_5": x_wait_for_process_output__mutmut_5,
    "x_wait_for_process_output__mutmut_6": x_wait_for_process_output__mutmut_6,
    "x_wait_for_process_output__mutmut_7": x_wait_for_process_output__mutmut_7,
    "x_wait_for_process_output__mutmut_8": x_wait_for_process_output__mutmut_8,
    "x_wait_for_process_output__mutmut_9": x_wait_for_process_output__mutmut_9,
    "x_wait_for_process_output__mutmut_10": x_wait_for_process_output__mutmut_10,
    "x_wait_for_process_output__mutmut_11": x_wait_for_process_output__mutmut_11,
    "x_wait_for_process_output__mutmut_12": x_wait_for_process_output__mutmut_12,
    "x_wait_for_process_output__mutmut_13": x_wait_for_process_output__mutmut_13,
    "x_wait_for_process_output__mutmut_14": x_wait_for_process_output__mutmut_14,
    "x_wait_for_process_output__mutmut_15": x_wait_for_process_output__mutmut_15,
    "x_wait_for_process_output__mutmut_16": x_wait_for_process_output__mutmut_16,
    "x_wait_for_process_output__mutmut_17": x_wait_for_process_output__mutmut_17,
    "x_wait_for_process_output__mutmut_18": x_wait_for_process_output__mutmut_18,
    "x_wait_for_process_output__mutmut_19": x_wait_for_process_output__mutmut_19,
    "x_wait_for_process_output__mutmut_20": x_wait_for_process_output__mutmut_20,
    "x_wait_for_process_output__mutmut_21": x_wait_for_process_output__mutmut_21,
    "x_wait_for_process_output__mutmut_22": x_wait_for_process_output__mutmut_22,
    "x_wait_for_process_output__mutmut_23": x_wait_for_process_output__mutmut_23,
    "x_wait_for_process_output__mutmut_24": x_wait_for_process_output__mutmut_24,
    "x_wait_for_process_output__mutmut_25": x_wait_for_process_output__mutmut_25,
    "x_wait_for_process_output__mutmut_26": x_wait_for_process_output__mutmut_26,
    "x_wait_for_process_output__mutmut_27": x_wait_for_process_output__mutmut_27,
    "x_wait_for_process_output__mutmut_28": x_wait_for_process_output__mutmut_28,
    "x_wait_for_process_output__mutmut_29": x_wait_for_process_output__mutmut_29,
    "x_wait_for_process_output__mutmut_30": x_wait_for_process_output__mutmut_30,
    "x_wait_for_process_output__mutmut_31": x_wait_for_process_output__mutmut_31,
    "x_wait_for_process_output__mutmut_32": x_wait_for_process_output__mutmut_32,
    "x_wait_for_process_output__mutmut_33": x_wait_for_process_output__mutmut_33,
    "x_wait_for_process_output__mutmut_34": x_wait_for_process_output__mutmut_34,
    "x_wait_for_process_output__mutmut_35": x_wait_for_process_output__mutmut_35,
    "x_wait_for_process_output__mutmut_36": x_wait_for_process_output__mutmut_36,
    "x_wait_for_process_output__mutmut_37": x_wait_for_process_output__mutmut_37,
    "x_wait_for_process_output__mutmut_38": x_wait_for_process_output__mutmut_38,
    "x_wait_for_process_output__mutmut_39": x_wait_for_process_output__mutmut_39,
    "x_wait_for_process_output__mutmut_40": x_wait_for_process_output__mutmut_40,
    "x_wait_for_process_output__mutmut_41": x_wait_for_process_output__mutmut_41,
    "x_wait_for_process_output__mutmut_42": x_wait_for_process_output__mutmut_42,
    "x_wait_for_process_output__mutmut_43": x_wait_for_process_output__mutmut_43,
    "x_wait_for_process_output__mutmut_44": x_wait_for_process_output__mutmut_44,
    "x_wait_for_process_output__mutmut_45": x_wait_for_process_output__mutmut_45,
    "x_wait_for_process_output__mutmut_46": x_wait_for_process_output__mutmut_46,
    "x_wait_for_process_output__mutmut_47": x_wait_for_process_output__mutmut_47,
    "x_wait_for_process_output__mutmut_48": x_wait_for_process_output__mutmut_48,
    "x_wait_for_process_output__mutmut_49": x_wait_for_process_output__mutmut_49,
    "x_wait_for_process_output__mutmut_50": x_wait_for_process_output__mutmut_50,
    "x_wait_for_process_output__mutmut_51": x_wait_for_process_output__mutmut_51,
    "x_wait_for_process_output__mutmut_52": x_wait_for_process_output__mutmut_52,
    "x_wait_for_process_output__mutmut_53": x_wait_for_process_output__mutmut_53,
    "x_wait_for_process_output__mutmut_54": x_wait_for_process_output__mutmut_54,
    "x_wait_for_process_output__mutmut_55": x_wait_for_process_output__mutmut_55,
    "x_wait_for_process_output__mutmut_56": x_wait_for_process_output__mutmut_56,
    "x_wait_for_process_output__mutmut_57": x_wait_for_process_output__mutmut_57,
    "x_wait_for_process_output__mutmut_58": x_wait_for_process_output__mutmut_58,
    "x_wait_for_process_output__mutmut_59": x_wait_for_process_output__mutmut_59,
    "x_wait_for_process_output__mutmut_60": x_wait_for_process_output__mutmut_60,
}


def wait_for_process_output(*args, **kwargs):
    result = _mutmut_trampoline(
        x_wait_for_process_output__mutmut_orig, x_wait_for_process_output__mutmut_mutants, args, kwargs
    )
    return result


wait_for_process_output.__signature__ = _mutmut_signature(x_wait_for_process_output__mutmut_orig)
x_wait_for_process_output__mutmut_orig.__name__ = "x_wait_for_process_output"


# <3 🧱🤝🏃🪄
