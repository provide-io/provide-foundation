# provide/foundation/file/temp.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Generator
import contextlib
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

from provide.foundation.config.defaults import (
    DEFAULT_TEMP_CLEANUP,
    DEFAULT_TEMP_PREFIX,
    DEFAULT_TEMP_SUFFIX,
    DEFAULT_TEMP_TEXT_MODE,
)
from provide.foundation.errors.handlers import error_boundary
from provide.foundation.file.safe import safe_delete
from provide.foundation.logger import get_logger

"""Temporary file and directory utilities."""

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


def x_system_temp_dir__mutmut_orig() -> Path:
    """Get the operating system's temporary directory.

    Returns:
        Path to the OS temp directory

    Example:
        >>> temp_path = system_temp_dir()
        >>> print(temp_path)  # e.g., /tmp or C:\\Users\\...\\Temp

    """
    return Path(tempfile.gettempdir())


def x_system_temp_dir__mutmut_1() -> Path:
    """Get the operating system's temporary directory.

    Returns:
        Path to the OS temp directory

    Example:
        >>> temp_path = system_temp_dir()
        >>> print(temp_path)  # e.g., /tmp or C:\\Users\\...\\Temp

    """
    return Path(None)

x_system_temp_dir__mutmut_mutants : ClassVar[MutantDict] = {
'x_system_temp_dir__mutmut_1': x_system_temp_dir__mutmut_1
}

def system_temp_dir(*args, **kwargs):
    result = _mutmut_trampoline(x_system_temp_dir__mutmut_orig, x_system_temp_dir__mutmut_mutants, args, kwargs)
    return result 

system_temp_dir.__signature__ = _mutmut_signature(x_system_temp_dir__mutmut_orig)
x_system_temp_dir__mutmut_orig.__name__ = 'x_system_temp_dir'


def x_secure_temp_file__mutmut_orig(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_1(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir or isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_2(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = None

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_3(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(None)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_4(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = None
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_5(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=None, prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_6(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=None, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_7(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=None)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_8(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(prefix=prefix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_9(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, dir=dir)
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_10(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, )
    return fd, Path(temp_path)


def x_secure_temp_file__mutmut_11(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
) -> tuple[int, Path]:
    """Create a secure temporary file with restricted permissions.

    This is similar to tempfile.mkstemp but uses Foundation's defaults.
    The file is created with permissions 0o600 (owner read/write only).

    Use this when you need:
    - Direct file descriptor access (for os.fdopen, os.fsync, etc.)
    - Atomic file operations
    - Maximum security (restricted permissions)

    Args:
        suffix: File suffix
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)

    Returns:
        Tuple of (file_descriptor, Path) - caller must close the fd

    Example:
        >>> fd, path = secure_temp_file(suffix='.tmp')
        >>> try:
        ...     with os.fdopen(fd, 'wb') as f:
        ...         f.write(b'data')
        ...         os.fsync(f.fileno())
        ... finally:
        ...     path.unlink(missing_ok=True)

    """
    if dir and isinstance(dir, Path):
        dir = str(dir)

    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    return fd, Path(None)

x_secure_temp_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_secure_temp_file__mutmut_1': x_secure_temp_file__mutmut_1, 
    'x_secure_temp_file__mutmut_2': x_secure_temp_file__mutmut_2, 
    'x_secure_temp_file__mutmut_3': x_secure_temp_file__mutmut_3, 
    'x_secure_temp_file__mutmut_4': x_secure_temp_file__mutmut_4, 
    'x_secure_temp_file__mutmut_5': x_secure_temp_file__mutmut_5, 
    'x_secure_temp_file__mutmut_6': x_secure_temp_file__mutmut_6, 
    'x_secure_temp_file__mutmut_7': x_secure_temp_file__mutmut_7, 
    'x_secure_temp_file__mutmut_8': x_secure_temp_file__mutmut_8, 
    'x_secure_temp_file__mutmut_9': x_secure_temp_file__mutmut_9, 
    'x_secure_temp_file__mutmut_10': x_secure_temp_file__mutmut_10, 
    'x_secure_temp_file__mutmut_11': x_secure_temp_file__mutmut_11
}

def secure_temp_file(*args, **kwargs):
    result = _mutmut_trampoline(x_secure_temp_file__mutmut_orig, x_secure_temp_file__mutmut_mutants, args, kwargs)
    return result 

secure_temp_file.__signature__ = _mutmut_signature(x_secure_temp_file__mutmut_orig)
x_secure_temp_file__mutmut_orig.__name__ = 'x_secure_temp_file'


@contextmanager
def temp_file(
    suffix: str = DEFAULT_TEMP_SUFFIX,
    prefix: str = DEFAULT_TEMP_PREFIX,
    dir: Path | str | None = None,
    text: bool = DEFAULT_TEMP_TEXT_MODE,
    cleanup: bool = DEFAULT_TEMP_CLEANUP,
) -> Generator[Path, None, None]:
    """Create a temporary file with automatic cleanup.

    Args:
        suffix: File suffix (e.g., '.txt', '.json')
        prefix: File name prefix
        dir: Directory for the temp file (None = system temp)
        text: Whether to open in text mode
        cleanup: Whether to remove file on exit

    Yields:
        Path object for the temporary file

    Example:
        >>> with temp_file(suffix='.json') as tmp:
        ...     tmp.write_text('{"key": "value"}')
        ...     process_file(tmp)

    """
    temp_path = None
    try:
        if dir and isinstance(dir, Path):
            dir = str(dir)

        # Create temp file and immediately close it
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            prefix=prefix,
            dir=dir,
            delete=False,
            mode="w" if text else "wb",
        ) as f:
            temp_path = Path(f.name)

        log.debug("Created temp file", path=str(temp_path))
        yield temp_path

    finally:
        if cleanup and temp_path and temp_path.exists():
            with error_boundary(Exception, reraise=False):
                safe_delete(temp_path, missing_ok=True)
                # Safe logging - catch ValueError/OSError for closed file streams during test teardown
                with contextlib.suppress(ValueError, OSError):
                    log.debug("Cleaned up temp file", path=str(temp_path))


@contextmanager
def temp_dir(
    prefix: str = DEFAULT_TEMP_PREFIX,
    cleanup: bool = DEFAULT_TEMP_CLEANUP,
) -> Generator[Path, None, None]:
    """Create temporary directory with automatic cleanup.

    Args:
        prefix: Directory name prefix
        cleanup: Whether to remove directory on exit

    Yields:
        Path object for the temporary directory

    Example:
        >>> with temp_dir() as tmpdir:
        ...     (tmpdir / 'data.txt').write_text('content')
        ...     process_directory(tmpdir)

    """
    temp_path = None
    try:
        temp_path = Path(tempfile.mkdtemp(prefix=prefix))
        log.debug("Created temp directory", path=str(temp_path))
        yield temp_path
    finally:
        if cleanup and temp_path and temp_path.exists():
            with error_boundary(Exception, reraise=False):
                shutil.rmtree(temp_path)
                # Safe logging - catch ValueError/OSError for closed file streams during test teardown
                with contextlib.suppress(ValueError, OSError):
                    log.debug("Cleaned up temp directory", path=str(temp_path))


# <3 🧱🤝📄🪄
