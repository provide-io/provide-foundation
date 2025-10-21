# provide/foundation/process/lifecycle/managed.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import Mapping
import functools
import os
from pathlib import Path
import subprocess
import sys
import threading
import traceback
from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.errors.process import ProcessError
from provide.foundation.errors.runtime import StateError
from provide.foundation.logger import get_logger
from provide.foundation.process.defaults import (
    DEFAULT_PROCESS_READCHAR_TIMEOUT,
    DEFAULT_PROCESS_READLINE_TIMEOUT,
    DEFAULT_PROCESS_TERMINATE_TIMEOUT,
)

"""Managed subprocess with lifecycle support.

This module provides the ManagedProcess class for managing long-running
subprocesses with proper lifecycle management and graceful shutdown.
"""

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


class ManagedProcess:
    """A managed subprocess with lifecycle support, monitoring, and graceful shutdown.

    This class wraps subprocess.Popen with additional functionality for:
    - Environment management
    - Output streaming and monitoring
    - Health checks and process monitoring
    - Graceful shutdown with timeouts
    - Background stderr relaying
    """

    def xǁManagedProcessǁ__init____mutmut_orig(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_1(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = False,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_2(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = True,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_3(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 1,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_4(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_5(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = None
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_6(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_7(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(None) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_8(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = None
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_9(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = None
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_10(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = None
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_11(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = None
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_12(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = None

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_13(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = None

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_14(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(None):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_15(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(None):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_16(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("XXCOVERAGEXX", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_17(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("coverage", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_18(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "XXCOV_COREXX")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_19(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "cov_core")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_20(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(None, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_21(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_22(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, )

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_23(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(None)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_24(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = ""
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_25(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = ""
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_26(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = None

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_27(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = True

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_28(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            None,
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_29(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=None,
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_30(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            cwd=None,
        )

    def xǁManagedProcessǁ__init____mutmut_31(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_32(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_33(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(command),
            )

    def xǁManagedProcessǁ__init____mutmut_34(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "XX🚀 ManagedProcess initializedXX",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_35(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 managedprocess initialized",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_36(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 MANAGEDPROCESS INITIALIZED",
            command=" ".join(command),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_37(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command=" ".join(None),
            cwd=self.cwd,
        )

    def xǁManagedProcessǁ__init____mutmut_38(
        self,
        command: list[str],
        *,
        cwd: str | Path | None = None,
        env: Mapping[str, str] | None = None,
        capture_output: bool = True,
        text_mode: bool = False,
        bufsize: int = 0,
        stderr_relay: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a ManagedProcess."""
        self.command = command
        self.cwd = str(cwd) if cwd else None
        self.capture_output = capture_output
        self.text_mode = text_mode
        self.bufsize = bufsize
        self.stderr_relay = stderr_relay
        self.kwargs = kwargs

        # Build environment - always start with current environment
        self._env = os.environ.copy()

        # Clean coverage-related environment variables from subprocess
        # to prevent interference with output capture during testing
        for key in list(self._env.keys()):
            if key.startswith(("COVERAGE", "COV_CORE")):
                self._env.pop(key, None)

        # Merge in any provided environment variables
        if env:
            self._env.update(env)

        # Process state
        self._process: subprocess.Popen[bytes] | None = None
        self._stderr_thread: threading.Thread | None = None
        self._started = False

        log.debug(
            "🚀 ManagedProcess initialized",
            command="XX XX".join(command),
            cwd=self.cwd,
        )
    
    xǁManagedProcessǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁ__init____mutmut_1': xǁManagedProcessǁ__init____mutmut_1, 
        'xǁManagedProcessǁ__init____mutmut_2': xǁManagedProcessǁ__init____mutmut_2, 
        'xǁManagedProcessǁ__init____mutmut_3': xǁManagedProcessǁ__init____mutmut_3, 
        'xǁManagedProcessǁ__init____mutmut_4': xǁManagedProcessǁ__init____mutmut_4, 
        'xǁManagedProcessǁ__init____mutmut_5': xǁManagedProcessǁ__init____mutmut_5, 
        'xǁManagedProcessǁ__init____mutmut_6': xǁManagedProcessǁ__init____mutmut_6, 
        'xǁManagedProcessǁ__init____mutmut_7': xǁManagedProcessǁ__init____mutmut_7, 
        'xǁManagedProcessǁ__init____mutmut_8': xǁManagedProcessǁ__init____mutmut_8, 
        'xǁManagedProcessǁ__init____mutmut_9': xǁManagedProcessǁ__init____mutmut_9, 
        'xǁManagedProcessǁ__init____mutmut_10': xǁManagedProcessǁ__init____mutmut_10, 
        'xǁManagedProcessǁ__init____mutmut_11': xǁManagedProcessǁ__init____mutmut_11, 
        'xǁManagedProcessǁ__init____mutmut_12': xǁManagedProcessǁ__init____mutmut_12, 
        'xǁManagedProcessǁ__init____mutmut_13': xǁManagedProcessǁ__init____mutmut_13, 
        'xǁManagedProcessǁ__init____mutmut_14': xǁManagedProcessǁ__init____mutmut_14, 
        'xǁManagedProcessǁ__init____mutmut_15': xǁManagedProcessǁ__init____mutmut_15, 
        'xǁManagedProcessǁ__init____mutmut_16': xǁManagedProcessǁ__init____mutmut_16, 
        'xǁManagedProcessǁ__init____mutmut_17': xǁManagedProcessǁ__init____mutmut_17, 
        'xǁManagedProcessǁ__init____mutmut_18': xǁManagedProcessǁ__init____mutmut_18, 
        'xǁManagedProcessǁ__init____mutmut_19': xǁManagedProcessǁ__init____mutmut_19, 
        'xǁManagedProcessǁ__init____mutmut_20': xǁManagedProcessǁ__init____mutmut_20, 
        'xǁManagedProcessǁ__init____mutmut_21': xǁManagedProcessǁ__init____mutmut_21, 
        'xǁManagedProcessǁ__init____mutmut_22': xǁManagedProcessǁ__init____mutmut_22, 
        'xǁManagedProcessǁ__init____mutmut_23': xǁManagedProcessǁ__init____mutmut_23, 
        'xǁManagedProcessǁ__init____mutmut_24': xǁManagedProcessǁ__init____mutmut_24, 
        'xǁManagedProcessǁ__init____mutmut_25': xǁManagedProcessǁ__init____mutmut_25, 
        'xǁManagedProcessǁ__init____mutmut_26': xǁManagedProcessǁ__init____mutmut_26, 
        'xǁManagedProcessǁ__init____mutmut_27': xǁManagedProcessǁ__init____mutmut_27, 
        'xǁManagedProcessǁ__init____mutmut_28': xǁManagedProcessǁ__init____mutmut_28, 
        'xǁManagedProcessǁ__init____mutmut_29': xǁManagedProcessǁ__init____mutmut_29, 
        'xǁManagedProcessǁ__init____mutmut_30': xǁManagedProcessǁ__init____mutmut_30, 
        'xǁManagedProcessǁ__init____mutmut_31': xǁManagedProcessǁ__init____mutmut_31, 
        'xǁManagedProcessǁ__init____mutmut_32': xǁManagedProcessǁ__init____mutmut_32, 
        'xǁManagedProcessǁ__init____mutmut_33': xǁManagedProcessǁ__init____mutmut_33, 
        'xǁManagedProcessǁ__init____mutmut_34': xǁManagedProcessǁ__init____mutmut_34, 
        'xǁManagedProcessǁ__init____mutmut_35': xǁManagedProcessǁ__init____mutmut_35, 
        'xǁManagedProcessǁ__init____mutmut_36': xǁManagedProcessǁ__init____mutmut_36, 
        'xǁManagedProcessǁ__init____mutmut_37': xǁManagedProcessǁ__init____mutmut_37, 
        'xǁManagedProcessǁ__init____mutmut_38': xǁManagedProcessǁ__init____mutmut_38
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁManagedProcessǁ__init____mutmut_orig)
    xǁManagedProcessǁ__init____mutmut_orig.__name__ = 'xǁManagedProcessǁ__init__'

    @property
    def process(self) -> subprocess.Popen[bytes] | None:
        """Get the underlying subprocess.Popen instance."""
        return self._process

    @property
    def pid(self) -> int | None:
        """Get the process ID, if process is running."""
        return self._process.pid if self._process else None

    @property
    def returncode(self) -> int | None:
        """Get the return code, if process has terminated."""
        return self._process.returncode if self._process else None

    def xǁManagedProcessǁis_running__mutmut_orig(self) -> bool:
        """Check if the process is currently running."""
        if not self._process:
            return False
        return self._process.poll() is None

    def xǁManagedProcessǁis_running__mutmut_1(self) -> bool:
        """Check if the process is currently running."""
        if self._process:
            return False
        return self._process.poll() is None

    def xǁManagedProcessǁis_running__mutmut_2(self) -> bool:
        """Check if the process is currently running."""
        if not self._process:
            return True
        return self._process.poll() is None

    def xǁManagedProcessǁis_running__mutmut_3(self) -> bool:
        """Check if the process is currently running."""
        if not self._process:
            return False
        return self._process.poll() is not None
    
    xǁManagedProcessǁis_running__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁis_running__mutmut_1': xǁManagedProcessǁis_running__mutmut_1, 
        'xǁManagedProcessǁis_running__mutmut_2': xǁManagedProcessǁis_running__mutmut_2, 
        'xǁManagedProcessǁis_running__mutmut_3': xǁManagedProcessǁis_running__mutmut_3
    }
    
    def is_running(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁis_running__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁis_running__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_running.__signature__ = _mutmut_signature(xǁManagedProcessǁis_running__mutmut_orig)
    xǁManagedProcessǁis_running__mutmut_orig.__name__ = 'xǁManagedProcessǁis_running'

    @resilient(
        error_mapper=lambda e: ProcessError(f"Failed to launch process: {e}")
        if not isinstance(e, (ProcessError, StateError))
        else e,
    )
    def launch(self) -> None:
        """Launch the managed process.

        Raises:
            ProcessError: If the process fails to launch
            StateError: If the process is already started

        """
        if self._started:
            raise StateError(
                "Process has already been started", code="PROCESS_ALREADY_STARTED", process_state="started"
            )

        log.debug("🚀 Launching managed process", command=" ".join(self.command))

        self._process = subprocess.Popen(
            self.command,
            cwd=self.cwd,
            env=self._env,
            stdout=subprocess.PIPE if self.capture_output else None,
            stderr=subprocess.PIPE if self.capture_output else None,
            text=self.text_mode,
            bufsize=self.bufsize,
            **self.kwargs,
        )
        self._started = True

        log.info(
            "🚀 Managed process started successfully",
            pid=self._process.pid,
            command=" ".join(self.command),
        )

        # Start stderr relay if enabled
        if self.stderr_relay and self._process.stderr:
            self._start_stderr_relay()

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_orig(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_1(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process and not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_2(self) -> None:
        """Start a background thread to relay stderr output."""
        if self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_3(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_4(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = None
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_5(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process and not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_6(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_7(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_8(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while False:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_9(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = None
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_10(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_11(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        return
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_12(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        None
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_13(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode(None, errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_14(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors=None) if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_15(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode(errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_16(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", ) if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_17(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("XXutf-8XX", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_18(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("UTF-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_19(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="XXreplaceXX") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_20(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="REPLACE") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_21(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(None)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_22(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug(None, error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_23(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=None)

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_24(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug(error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_25(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", )

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_26(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("XXError in stderr relayXX", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_27(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_28(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("ERROR IN STDERR RELAY", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_29(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(None))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_30(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = None
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_31(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=None, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_32(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=None)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_33(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_34(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, )
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_35(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=False)
        self._stderr_thread.start()
        log.debug("🚀 Started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_36(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug(None)

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_37(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("XX🚀 Started stderr relay threadXX")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_38(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 started stderr relay thread")

    def xǁManagedProcessǁ_start_stderr_relay__mutmut_39(self) -> None:
        """Start a background thread to relay stderr output."""
        if not self._process or not self._process.stderr:
            return

        def relay_stderr() -> None:
            """Relay stderr output to the current process stderr."""
            process = self._process
            if not process or not process.stderr:
                return

            try:
                while True:
                    line = process.stderr.readline()
                    if not line:
                        break
                    sys.stderr.write(
                        line.decode("utf-8", errors="replace") if isinstance(line, bytes) else str(line)
                    )
                    sys.stderr.flush()
            except Exception as e:
                log.debug("Error in stderr relay", error=str(e))

        self._stderr_thread = threading.Thread(target=relay_stderr, daemon=True)
        self._stderr_thread.start()
        log.debug("🚀 STARTED STDERR RELAY THREAD")
    
    xǁManagedProcessǁ_start_stderr_relay__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁ_start_stderr_relay__mutmut_1': xǁManagedProcessǁ_start_stderr_relay__mutmut_1, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_2': xǁManagedProcessǁ_start_stderr_relay__mutmut_2, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_3': xǁManagedProcessǁ_start_stderr_relay__mutmut_3, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_4': xǁManagedProcessǁ_start_stderr_relay__mutmut_4, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_5': xǁManagedProcessǁ_start_stderr_relay__mutmut_5, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_6': xǁManagedProcessǁ_start_stderr_relay__mutmut_6, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_7': xǁManagedProcessǁ_start_stderr_relay__mutmut_7, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_8': xǁManagedProcessǁ_start_stderr_relay__mutmut_8, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_9': xǁManagedProcessǁ_start_stderr_relay__mutmut_9, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_10': xǁManagedProcessǁ_start_stderr_relay__mutmut_10, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_11': xǁManagedProcessǁ_start_stderr_relay__mutmut_11, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_12': xǁManagedProcessǁ_start_stderr_relay__mutmut_12, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_13': xǁManagedProcessǁ_start_stderr_relay__mutmut_13, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_14': xǁManagedProcessǁ_start_stderr_relay__mutmut_14, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_15': xǁManagedProcessǁ_start_stderr_relay__mutmut_15, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_16': xǁManagedProcessǁ_start_stderr_relay__mutmut_16, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_17': xǁManagedProcessǁ_start_stderr_relay__mutmut_17, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_18': xǁManagedProcessǁ_start_stderr_relay__mutmut_18, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_19': xǁManagedProcessǁ_start_stderr_relay__mutmut_19, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_20': xǁManagedProcessǁ_start_stderr_relay__mutmut_20, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_21': xǁManagedProcessǁ_start_stderr_relay__mutmut_21, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_22': xǁManagedProcessǁ_start_stderr_relay__mutmut_22, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_23': xǁManagedProcessǁ_start_stderr_relay__mutmut_23, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_24': xǁManagedProcessǁ_start_stderr_relay__mutmut_24, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_25': xǁManagedProcessǁ_start_stderr_relay__mutmut_25, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_26': xǁManagedProcessǁ_start_stderr_relay__mutmut_26, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_27': xǁManagedProcessǁ_start_stderr_relay__mutmut_27, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_28': xǁManagedProcessǁ_start_stderr_relay__mutmut_28, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_29': xǁManagedProcessǁ_start_stderr_relay__mutmut_29, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_30': xǁManagedProcessǁ_start_stderr_relay__mutmut_30, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_31': xǁManagedProcessǁ_start_stderr_relay__mutmut_31, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_32': xǁManagedProcessǁ_start_stderr_relay__mutmut_32, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_33': xǁManagedProcessǁ_start_stderr_relay__mutmut_33, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_34': xǁManagedProcessǁ_start_stderr_relay__mutmut_34, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_35': xǁManagedProcessǁ_start_stderr_relay__mutmut_35, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_36': xǁManagedProcessǁ_start_stderr_relay__mutmut_36, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_37': xǁManagedProcessǁ_start_stderr_relay__mutmut_37, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_38': xǁManagedProcessǁ_start_stderr_relay__mutmut_38, 
        'xǁManagedProcessǁ_start_stderr_relay__mutmut_39': xǁManagedProcessǁ_start_stderr_relay__mutmut_39
    }
    
    def _start_stderr_relay(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁ_start_stderr_relay__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁ_start_stderr_relay__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _start_stderr_relay.__signature__ = _mutmut_signature(xǁManagedProcessǁ_start_stderr_relay__mutmut_orig)
    xǁManagedProcessǁ_start_stderr_relay__mutmut_orig.__name__ = 'xǁManagedProcessǁ_start_stderr_relay'

    async def xǁManagedProcessǁread_line_async__mutmut_orig(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_1(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process and not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_2(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_3(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_4(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError(None)

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_5(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("XXProcess not running or stdout not availableXX")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_6(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_7(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("PROCESS NOT RUNNING OR STDOUT NOT AVAILABLE")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_8(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = None

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_9(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = None

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_10(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(None)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_11(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = None
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_12(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(None, timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_13(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=None)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_14(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_15(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), )
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_16(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, None), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_17(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_18(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, ), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_19(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode(None, errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_20(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors=None) if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_21(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode(errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_22(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", ) if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_23(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("XXutf-8XX", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_24(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("UTF-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_25(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="XXreplaceXX") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_26(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="REPLACE") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_27(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(None)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_28(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug(None)
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_29(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("XXRead timeout on managed process stdoutXX")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_30(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("read timeout on managed process stdout")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_31(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("READ TIMEOUT ON MANAGED PROCESS STDOUT")
            raise TimeoutError(f"Read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_line_async__mutmut_32(self, timeout: float = DEFAULT_PROCESS_READLINE_TIMEOUT) -> str:
        """Read a line from stdout asynchronously with timeout."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.readline)

        try:
            line_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            return (
                line_data.decode("utf-8", errors="replace") if isinstance(line_data, bytes) else str(line_data)
            ).strip()
        except TimeoutError as e:
            log.debug("Read timeout on managed process stdout")
            raise TimeoutError(None) from e
    
    xǁManagedProcessǁread_line_async__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁread_line_async__mutmut_1': xǁManagedProcessǁread_line_async__mutmut_1, 
        'xǁManagedProcessǁread_line_async__mutmut_2': xǁManagedProcessǁread_line_async__mutmut_2, 
        'xǁManagedProcessǁread_line_async__mutmut_3': xǁManagedProcessǁread_line_async__mutmut_3, 
        'xǁManagedProcessǁread_line_async__mutmut_4': xǁManagedProcessǁread_line_async__mutmut_4, 
        'xǁManagedProcessǁread_line_async__mutmut_5': xǁManagedProcessǁread_line_async__mutmut_5, 
        'xǁManagedProcessǁread_line_async__mutmut_6': xǁManagedProcessǁread_line_async__mutmut_6, 
        'xǁManagedProcessǁread_line_async__mutmut_7': xǁManagedProcessǁread_line_async__mutmut_7, 
        'xǁManagedProcessǁread_line_async__mutmut_8': xǁManagedProcessǁread_line_async__mutmut_8, 
        'xǁManagedProcessǁread_line_async__mutmut_9': xǁManagedProcessǁread_line_async__mutmut_9, 
        'xǁManagedProcessǁread_line_async__mutmut_10': xǁManagedProcessǁread_line_async__mutmut_10, 
        'xǁManagedProcessǁread_line_async__mutmut_11': xǁManagedProcessǁread_line_async__mutmut_11, 
        'xǁManagedProcessǁread_line_async__mutmut_12': xǁManagedProcessǁread_line_async__mutmut_12, 
        'xǁManagedProcessǁread_line_async__mutmut_13': xǁManagedProcessǁread_line_async__mutmut_13, 
        'xǁManagedProcessǁread_line_async__mutmut_14': xǁManagedProcessǁread_line_async__mutmut_14, 
        'xǁManagedProcessǁread_line_async__mutmut_15': xǁManagedProcessǁread_line_async__mutmut_15, 
        'xǁManagedProcessǁread_line_async__mutmut_16': xǁManagedProcessǁread_line_async__mutmut_16, 
        'xǁManagedProcessǁread_line_async__mutmut_17': xǁManagedProcessǁread_line_async__mutmut_17, 
        'xǁManagedProcessǁread_line_async__mutmut_18': xǁManagedProcessǁread_line_async__mutmut_18, 
        'xǁManagedProcessǁread_line_async__mutmut_19': xǁManagedProcessǁread_line_async__mutmut_19, 
        'xǁManagedProcessǁread_line_async__mutmut_20': xǁManagedProcessǁread_line_async__mutmut_20, 
        'xǁManagedProcessǁread_line_async__mutmut_21': xǁManagedProcessǁread_line_async__mutmut_21, 
        'xǁManagedProcessǁread_line_async__mutmut_22': xǁManagedProcessǁread_line_async__mutmut_22, 
        'xǁManagedProcessǁread_line_async__mutmut_23': xǁManagedProcessǁread_line_async__mutmut_23, 
        'xǁManagedProcessǁread_line_async__mutmut_24': xǁManagedProcessǁread_line_async__mutmut_24, 
        'xǁManagedProcessǁread_line_async__mutmut_25': xǁManagedProcessǁread_line_async__mutmut_25, 
        'xǁManagedProcessǁread_line_async__mutmut_26': xǁManagedProcessǁread_line_async__mutmut_26, 
        'xǁManagedProcessǁread_line_async__mutmut_27': xǁManagedProcessǁread_line_async__mutmut_27, 
        'xǁManagedProcessǁread_line_async__mutmut_28': xǁManagedProcessǁread_line_async__mutmut_28, 
        'xǁManagedProcessǁread_line_async__mutmut_29': xǁManagedProcessǁread_line_async__mutmut_29, 
        'xǁManagedProcessǁread_line_async__mutmut_30': xǁManagedProcessǁread_line_async__mutmut_30, 
        'xǁManagedProcessǁread_line_async__mutmut_31': xǁManagedProcessǁread_line_async__mutmut_31, 
        'xǁManagedProcessǁread_line_async__mutmut_32': xǁManagedProcessǁread_line_async__mutmut_32
    }
    
    def read_line_async(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁread_line_async__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁread_line_async__mutmut_mutants"), args, kwargs, self)
        return result 
    
    read_line_async.__signature__ = _mutmut_signature(xǁManagedProcessǁread_line_async__mutmut_orig)
    xǁManagedProcessǁread_line_async__mutmut_orig.__name__ = 'xǁManagedProcessǁread_line_async'

    async def xǁManagedProcessǁread_char_async__mutmut_orig(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_1(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process and not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_2(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_3(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_4(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError(None)

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_5(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("XXProcess not running or stdout not availableXX")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_6(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_7(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("PROCESS NOT RUNNING OR STDOUT NOT AVAILABLE")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_8(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = None

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_9(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = None

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_10(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(None, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_11(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, None)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_12(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_13(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, )

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_14(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 2)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_15(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = None
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_16(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(None, timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_17(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=None)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_18(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_19(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), )
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_20(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, None), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_21(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_22(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, ), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_23(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_24(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return "XXXX"
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_25(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode(None, errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_26(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors=None) if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_27(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode(errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_28(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", ) if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_29(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("XXutf-8XX", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_30(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("UTF-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_31(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="XXreplaceXX") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_32(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="REPLACE") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_33(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(None)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_34(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug(None)
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_35(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("XXCharacter read timeout on managed process stdoutXX")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_36(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("character read timeout on managed process stdout")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_37(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("CHARACTER READ TIMEOUT ON MANAGED PROCESS STDOUT")
            raise TimeoutError(f"Character read timeout after {timeout}s") from e

    async def xǁManagedProcessǁread_char_async__mutmut_38(self, timeout: float = DEFAULT_PROCESS_READCHAR_TIMEOUT) -> str:
        """Read a single character from stdout asynchronously."""
        if not self._process or not self._process.stdout:
            raise ProcessError("Process not running or stdout not available")

        loop = asyncio.get_event_loop()

        # Use functools.partial to avoid closure issues
        read_func = functools.partial(self._process.stdout.read, 1)

        try:
            char_data = await asyncio.wait_for(loop.run_in_executor(None, read_func), timeout=timeout)
            if not char_data:
                return ""
            return (
                char_data.decode("utf-8", errors="replace") if isinstance(char_data, bytes) else str(char_data)
            )
        except TimeoutError as e:
            log.debug("Character read timeout on managed process stdout")
            raise TimeoutError(None) from e
    
    xǁManagedProcessǁread_char_async__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁread_char_async__mutmut_1': xǁManagedProcessǁread_char_async__mutmut_1, 
        'xǁManagedProcessǁread_char_async__mutmut_2': xǁManagedProcessǁread_char_async__mutmut_2, 
        'xǁManagedProcessǁread_char_async__mutmut_3': xǁManagedProcessǁread_char_async__mutmut_3, 
        'xǁManagedProcessǁread_char_async__mutmut_4': xǁManagedProcessǁread_char_async__mutmut_4, 
        'xǁManagedProcessǁread_char_async__mutmut_5': xǁManagedProcessǁread_char_async__mutmut_5, 
        'xǁManagedProcessǁread_char_async__mutmut_6': xǁManagedProcessǁread_char_async__mutmut_6, 
        'xǁManagedProcessǁread_char_async__mutmut_7': xǁManagedProcessǁread_char_async__mutmut_7, 
        'xǁManagedProcessǁread_char_async__mutmut_8': xǁManagedProcessǁread_char_async__mutmut_8, 
        'xǁManagedProcessǁread_char_async__mutmut_9': xǁManagedProcessǁread_char_async__mutmut_9, 
        'xǁManagedProcessǁread_char_async__mutmut_10': xǁManagedProcessǁread_char_async__mutmut_10, 
        'xǁManagedProcessǁread_char_async__mutmut_11': xǁManagedProcessǁread_char_async__mutmut_11, 
        'xǁManagedProcessǁread_char_async__mutmut_12': xǁManagedProcessǁread_char_async__mutmut_12, 
        'xǁManagedProcessǁread_char_async__mutmut_13': xǁManagedProcessǁread_char_async__mutmut_13, 
        'xǁManagedProcessǁread_char_async__mutmut_14': xǁManagedProcessǁread_char_async__mutmut_14, 
        'xǁManagedProcessǁread_char_async__mutmut_15': xǁManagedProcessǁread_char_async__mutmut_15, 
        'xǁManagedProcessǁread_char_async__mutmut_16': xǁManagedProcessǁread_char_async__mutmut_16, 
        'xǁManagedProcessǁread_char_async__mutmut_17': xǁManagedProcessǁread_char_async__mutmut_17, 
        'xǁManagedProcessǁread_char_async__mutmut_18': xǁManagedProcessǁread_char_async__mutmut_18, 
        'xǁManagedProcessǁread_char_async__mutmut_19': xǁManagedProcessǁread_char_async__mutmut_19, 
        'xǁManagedProcessǁread_char_async__mutmut_20': xǁManagedProcessǁread_char_async__mutmut_20, 
        'xǁManagedProcessǁread_char_async__mutmut_21': xǁManagedProcessǁread_char_async__mutmut_21, 
        'xǁManagedProcessǁread_char_async__mutmut_22': xǁManagedProcessǁread_char_async__mutmut_22, 
        'xǁManagedProcessǁread_char_async__mutmut_23': xǁManagedProcessǁread_char_async__mutmut_23, 
        'xǁManagedProcessǁread_char_async__mutmut_24': xǁManagedProcessǁread_char_async__mutmut_24, 
        'xǁManagedProcessǁread_char_async__mutmut_25': xǁManagedProcessǁread_char_async__mutmut_25, 
        'xǁManagedProcessǁread_char_async__mutmut_26': xǁManagedProcessǁread_char_async__mutmut_26, 
        'xǁManagedProcessǁread_char_async__mutmut_27': xǁManagedProcessǁread_char_async__mutmut_27, 
        'xǁManagedProcessǁread_char_async__mutmut_28': xǁManagedProcessǁread_char_async__mutmut_28, 
        'xǁManagedProcessǁread_char_async__mutmut_29': xǁManagedProcessǁread_char_async__mutmut_29, 
        'xǁManagedProcessǁread_char_async__mutmut_30': xǁManagedProcessǁread_char_async__mutmut_30, 
        'xǁManagedProcessǁread_char_async__mutmut_31': xǁManagedProcessǁread_char_async__mutmut_31, 
        'xǁManagedProcessǁread_char_async__mutmut_32': xǁManagedProcessǁread_char_async__mutmut_32, 
        'xǁManagedProcessǁread_char_async__mutmut_33': xǁManagedProcessǁread_char_async__mutmut_33, 
        'xǁManagedProcessǁread_char_async__mutmut_34': xǁManagedProcessǁread_char_async__mutmut_34, 
        'xǁManagedProcessǁread_char_async__mutmut_35': xǁManagedProcessǁread_char_async__mutmut_35, 
        'xǁManagedProcessǁread_char_async__mutmut_36': xǁManagedProcessǁread_char_async__mutmut_36, 
        'xǁManagedProcessǁread_char_async__mutmut_37': xǁManagedProcessǁread_char_async__mutmut_37, 
        'xǁManagedProcessǁread_char_async__mutmut_38': xǁManagedProcessǁread_char_async__mutmut_38
    }
    
    def read_char_async(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁread_char_async__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁread_char_async__mutmut_mutants"), args, kwargs, self)
        return result 
    
    read_char_async.__signature__ = _mutmut_signature(xǁManagedProcessǁread_char_async__mutmut_orig)
    xǁManagedProcessǁread_char_async__mutmut_orig.__name__ = 'xǁManagedProcessǁread_char_async'

    def xǁManagedProcessǁterminate_gracefully__mutmut_orig(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_1(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_2(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return False

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_3(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_4(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug(None, returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_5(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=None)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_6(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug(returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_7(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", )
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_8(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("XXProcess already terminatedXX", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_9(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_10(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("PROCESS ALREADY TERMINATED", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_11(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return False

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_12(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug(None, pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_13(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=None)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_14(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug(pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_15(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", )

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_16(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("XX🛑 Terminating managed process gracefullyXX", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_17(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_18(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 TERMINATING MANAGED PROCESS GRACEFULLY", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_19(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug(None, pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_20(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=None)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_21(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug(pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_22(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", )

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_23(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("XX🛑 Sent SIGTERM to processXX", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_24(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 sent sigterm to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_25(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 SENT SIGTERM TO PROCESS", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_26(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=None)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_27(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info(None, pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_28(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=None)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_29(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info(pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_30(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", )
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_31(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("XX🛑 Process terminated gracefullyXX", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_32(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_33(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 PROCESS TERMINATED GRACEFULLY", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_34(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return False
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_35(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    None,
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_36(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=None,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_37(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_38(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_39(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "XX🛑 Process did not terminate gracefully, force killingXX",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_40(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_41(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 PROCESS DID NOT TERMINATE GRACEFULLY, FORCE KILLING",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_42(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=None)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_43(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=3.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_44(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info(None, pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_45(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=None)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_46(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info(pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_47(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", )
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_48(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("XX🛑 Process force killedXX", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_49(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_50(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 PROCESS FORCE KILLED", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_51(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return True
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_52(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error(None, pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_53(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=None)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_54(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error(pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_55(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", )
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_56(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("XX🛑 Process could not be killedXX", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_57(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_58(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 PROCESS COULD NOT BE KILLED", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_59(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return True

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_60(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                None,
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_61(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_62(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=None,
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_63(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=None,
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_64(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_65(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_66(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_67(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_68(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "XX🛑❌ Error terminating processXX",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_69(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_70(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ ERROR TERMINATING PROCESS",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_71(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(None),
                trace=traceback.format_exc(),
            )
            return False

    def xǁManagedProcessǁterminate_gracefully__mutmut_72(self, timeout: float = DEFAULT_PROCESS_TERMINATE_TIMEOUT) -> bool:
        """Terminate the process gracefully with a timeout.

        Args:
            timeout: Maximum time to wait for graceful termination

        Returns:
            True if process terminated gracefully, False if force-killed

        """
        if not self._process:
            return True

        if self._process.poll() is not None:
            log.debug("Process already terminated", returncode=self._process.returncode)
            return True

        log.debug("🛑 Terminating managed process gracefully", pid=self._process.pid)

        try:
            # Send SIGTERM
            self._process.terminate()
            log.debug("🛑 Sent SIGTERM to process", pid=self._process.pid)

            # Wait for graceful termination
            try:
                self._process.wait(timeout=timeout)
                log.info("🛑 Process terminated gracefully", pid=self._process.pid)
                return True
            except subprocess.TimeoutExpired:
                log.warning(
                    "🛑 Process did not terminate gracefully, force killing",
                    pid=self._process.pid,
                )
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=2.0)
                    log.info("🛑 Process force killed", pid=self._process.pid)
                    return False
                except subprocess.TimeoutExpired:
                    log.error("🛑 Process could not be killed", pid=self._process.pid)
                    return False

        except Exception as e:
            log.error(
                "🛑❌ Error terminating process",
                pid=self._process.pid if self._process else None,
                error=str(e),
                trace=traceback.format_exc(),
            )
            return True
    
    xǁManagedProcessǁterminate_gracefully__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁterminate_gracefully__mutmut_1': xǁManagedProcessǁterminate_gracefully__mutmut_1, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_2': xǁManagedProcessǁterminate_gracefully__mutmut_2, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_3': xǁManagedProcessǁterminate_gracefully__mutmut_3, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_4': xǁManagedProcessǁterminate_gracefully__mutmut_4, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_5': xǁManagedProcessǁterminate_gracefully__mutmut_5, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_6': xǁManagedProcessǁterminate_gracefully__mutmut_6, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_7': xǁManagedProcessǁterminate_gracefully__mutmut_7, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_8': xǁManagedProcessǁterminate_gracefully__mutmut_8, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_9': xǁManagedProcessǁterminate_gracefully__mutmut_9, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_10': xǁManagedProcessǁterminate_gracefully__mutmut_10, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_11': xǁManagedProcessǁterminate_gracefully__mutmut_11, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_12': xǁManagedProcessǁterminate_gracefully__mutmut_12, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_13': xǁManagedProcessǁterminate_gracefully__mutmut_13, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_14': xǁManagedProcessǁterminate_gracefully__mutmut_14, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_15': xǁManagedProcessǁterminate_gracefully__mutmut_15, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_16': xǁManagedProcessǁterminate_gracefully__mutmut_16, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_17': xǁManagedProcessǁterminate_gracefully__mutmut_17, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_18': xǁManagedProcessǁterminate_gracefully__mutmut_18, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_19': xǁManagedProcessǁterminate_gracefully__mutmut_19, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_20': xǁManagedProcessǁterminate_gracefully__mutmut_20, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_21': xǁManagedProcessǁterminate_gracefully__mutmut_21, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_22': xǁManagedProcessǁterminate_gracefully__mutmut_22, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_23': xǁManagedProcessǁterminate_gracefully__mutmut_23, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_24': xǁManagedProcessǁterminate_gracefully__mutmut_24, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_25': xǁManagedProcessǁterminate_gracefully__mutmut_25, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_26': xǁManagedProcessǁterminate_gracefully__mutmut_26, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_27': xǁManagedProcessǁterminate_gracefully__mutmut_27, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_28': xǁManagedProcessǁterminate_gracefully__mutmut_28, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_29': xǁManagedProcessǁterminate_gracefully__mutmut_29, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_30': xǁManagedProcessǁterminate_gracefully__mutmut_30, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_31': xǁManagedProcessǁterminate_gracefully__mutmut_31, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_32': xǁManagedProcessǁterminate_gracefully__mutmut_32, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_33': xǁManagedProcessǁterminate_gracefully__mutmut_33, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_34': xǁManagedProcessǁterminate_gracefully__mutmut_34, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_35': xǁManagedProcessǁterminate_gracefully__mutmut_35, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_36': xǁManagedProcessǁterminate_gracefully__mutmut_36, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_37': xǁManagedProcessǁterminate_gracefully__mutmut_37, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_38': xǁManagedProcessǁterminate_gracefully__mutmut_38, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_39': xǁManagedProcessǁterminate_gracefully__mutmut_39, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_40': xǁManagedProcessǁterminate_gracefully__mutmut_40, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_41': xǁManagedProcessǁterminate_gracefully__mutmut_41, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_42': xǁManagedProcessǁterminate_gracefully__mutmut_42, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_43': xǁManagedProcessǁterminate_gracefully__mutmut_43, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_44': xǁManagedProcessǁterminate_gracefully__mutmut_44, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_45': xǁManagedProcessǁterminate_gracefully__mutmut_45, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_46': xǁManagedProcessǁterminate_gracefully__mutmut_46, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_47': xǁManagedProcessǁterminate_gracefully__mutmut_47, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_48': xǁManagedProcessǁterminate_gracefully__mutmut_48, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_49': xǁManagedProcessǁterminate_gracefully__mutmut_49, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_50': xǁManagedProcessǁterminate_gracefully__mutmut_50, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_51': xǁManagedProcessǁterminate_gracefully__mutmut_51, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_52': xǁManagedProcessǁterminate_gracefully__mutmut_52, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_53': xǁManagedProcessǁterminate_gracefully__mutmut_53, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_54': xǁManagedProcessǁterminate_gracefully__mutmut_54, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_55': xǁManagedProcessǁterminate_gracefully__mutmut_55, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_56': xǁManagedProcessǁterminate_gracefully__mutmut_56, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_57': xǁManagedProcessǁterminate_gracefully__mutmut_57, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_58': xǁManagedProcessǁterminate_gracefully__mutmut_58, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_59': xǁManagedProcessǁterminate_gracefully__mutmut_59, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_60': xǁManagedProcessǁterminate_gracefully__mutmut_60, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_61': xǁManagedProcessǁterminate_gracefully__mutmut_61, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_62': xǁManagedProcessǁterminate_gracefully__mutmut_62, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_63': xǁManagedProcessǁterminate_gracefully__mutmut_63, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_64': xǁManagedProcessǁterminate_gracefully__mutmut_64, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_65': xǁManagedProcessǁterminate_gracefully__mutmut_65, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_66': xǁManagedProcessǁterminate_gracefully__mutmut_66, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_67': xǁManagedProcessǁterminate_gracefully__mutmut_67, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_68': xǁManagedProcessǁterminate_gracefully__mutmut_68, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_69': xǁManagedProcessǁterminate_gracefully__mutmut_69, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_70': xǁManagedProcessǁterminate_gracefully__mutmut_70, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_71': xǁManagedProcessǁterminate_gracefully__mutmut_71, 
        'xǁManagedProcessǁterminate_gracefully__mutmut_72': xǁManagedProcessǁterminate_gracefully__mutmut_72
    }
    
    def terminate_gracefully(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁterminate_gracefully__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁterminate_gracefully__mutmut_mutants"), args, kwargs, self)
        return result 
    
    terminate_gracefully.__signature__ = _mutmut_signature(xǁManagedProcessǁterminate_gracefully__mutmut_orig)
    xǁManagedProcessǁterminate_gracefully__mutmut_orig.__name__ = 'xǁManagedProcessǁterminate_gracefully'

    def xǁManagedProcessǁcleanup__mutmut_orig(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 Managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_1(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread or self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 Managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_2(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=None)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 Managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_3(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=2.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 Managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_4(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = ""

        log.debug("🧹 Managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_5(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug(None)

    def xǁManagedProcessǁcleanup__mutmut_6(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("XX🧹 Managed process cleanup completedXX")

    def xǁManagedProcessǁcleanup__mutmut_7(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 managed process cleanup completed")

    def xǁManagedProcessǁcleanup__mutmut_8(self) -> None:
        """Clean up process resources."""
        # Join stderr relay thread
        if self._stderr_thread and self._stderr_thread.is_alive():
            # Give it a moment to finish
            self._stderr_thread.join(timeout=1.0)

        # Clean up process reference
        if self._process:
            self._process = None

        log.debug("🧹 MANAGED PROCESS CLEANUP COMPLETED")
    
    xǁManagedProcessǁcleanup__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁManagedProcessǁcleanup__mutmut_1': xǁManagedProcessǁcleanup__mutmut_1, 
        'xǁManagedProcessǁcleanup__mutmut_2': xǁManagedProcessǁcleanup__mutmut_2, 
        'xǁManagedProcessǁcleanup__mutmut_3': xǁManagedProcessǁcleanup__mutmut_3, 
        'xǁManagedProcessǁcleanup__mutmut_4': xǁManagedProcessǁcleanup__mutmut_4, 
        'xǁManagedProcessǁcleanup__mutmut_5': xǁManagedProcessǁcleanup__mutmut_5, 
        'xǁManagedProcessǁcleanup__mutmut_6': xǁManagedProcessǁcleanup__mutmut_6, 
        'xǁManagedProcessǁcleanup__mutmut_7': xǁManagedProcessǁcleanup__mutmut_7, 
        'xǁManagedProcessǁcleanup__mutmut_8': xǁManagedProcessǁcleanup__mutmut_8
    }
    
    def cleanup(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁManagedProcessǁcleanup__mutmut_orig"), object.__getattribute__(self, "xǁManagedProcessǁcleanup__mutmut_mutants"), args, kwargs, self)
        return result 
    
    cleanup.__signature__ = _mutmut_signature(xǁManagedProcessǁcleanup__mutmut_orig)
    xǁManagedProcessǁcleanup__mutmut_orig.__name__ = 'xǁManagedProcessǁcleanup'

    def __enter__(self) -> ManagedProcess:
        """Context manager entry."""
        self.launch()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit with cleanup."""
        self.terminate_gracefully()
        self.cleanup()


# <3 🧱🤝🏃🪄
