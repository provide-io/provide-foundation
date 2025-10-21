# provide/foundation/file/utils.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

from provide.foundation.logger import get_logger

"""File utility functions."""

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


def x_get_size__mutmut_orig(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_1(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = None

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_2(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(None)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_3(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 1
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_4(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning(None, path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_5(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=None, error=str(e))
        return 0


def x_get_size__mutmut_6(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=None)
        return 0


def x_get_size__mutmut_7(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning(path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_8(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", error=str(e))
        return 0


def x_get_size__mutmut_9(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), )
        return 0


def x_get_size__mutmut_10(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("XXFailed to get file sizeXX", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_11(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("failed to get file size", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_12(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("FAILED TO GET FILE SIZE", path=str(path), error=str(e))
        return 0


def x_get_size__mutmut_13(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(None), error=str(e))
        return 0


def x_get_size__mutmut_14(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(None))
        return 0


def x_get_size__mutmut_15(path: Path | str) -> int:
    """Get file size in bytes, 0 if not exists.

    Args:
        path: File path

    Returns:
        Size in bytes, or 0 if file doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0
    except Exception as e:
        log.warning("Failed to get file size", path=str(path), error=str(e))
        return 1

x_get_size__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_size__mutmut_1': x_get_size__mutmut_1, 
    'x_get_size__mutmut_2': x_get_size__mutmut_2, 
    'x_get_size__mutmut_3': x_get_size__mutmut_3, 
    'x_get_size__mutmut_4': x_get_size__mutmut_4, 
    'x_get_size__mutmut_5': x_get_size__mutmut_5, 
    'x_get_size__mutmut_6': x_get_size__mutmut_6, 
    'x_get_size__mutmut_7': x_get_size__mutmut_7, 
    'x_get_size__mutmut_8': x_get_size__mutmut_8, 
    'x_get_size__mutmut_9': x_get_size__mutmut_9, 
    'x_get_size__mutmut_10': x_get_size__mutmut_10, 
    'x_get_size__mutmut_11': x_get_size__mutmut_11, 
    'x_get_size__mutmut_12': x_get_size__mutmut_12, 
    'x_get_size__mutmut_13': x_get_size__mutmut_13, 
    'x_get_size__mutmut_14': x_get_size__mutmut_14, 
    'x_get_size__mutmut_15': x_get_size__mutmut_15
}

def get_size(*args, **kwargs):
    result = _mutmut_trampoline(x_get_size__mutmut_orig, x_get_size__mutmut_mutants, args, kwargs)
    return result 

get_size.__signature__ = _mutmut_signature(x_get_size__mutmut_orig)
x_get_size__mutmut_orig.__name__ = 'x_get_size'


def x_get_mtime__mutmut_orig(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_1(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = None

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_2(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(None)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_3(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning(None, path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_4(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=None, error=str(e))
        return None


def x_get_mtime__mutmut_5(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=None)
        return None


def x_get_mtime__mutmut_6(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning(path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_7(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", error=str(e))
        return None


def x_get_mtime__mutmut_8(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), )
        return None


def x_get_mtime__mutmut_9(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("XXFailed to get modification timeXX", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_10(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("failed to get modification time", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_11(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("FAILED TO GET MODIFICATION TIME", path=str(path), error=str(e))
        return None


def x_get_mtime__mutmut_12(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(None), error=str(e))
        return None


def x_get_mtime__mutmut_13(path: Path | str) -> float | None:
    """Get modification time, None if not exists.

    Args:
        path: File path

    Returns:
        Modification time as timestamp, or None if doesn't exist

    """
    path = Path(path)

    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None
    except Exception as e:
        log.warning("Failed to get modification time", path=str(path), error=str(None))
        return None

x_get_mtime__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_mtime__mutmut_1': x_get_mtime__mutmut_1, 
    'x_get_mtime__mutmut_2': x_get_mtime__mutmut_2, 
    'x_get_mtime__mutmut_3': x_get_mtime__mutmut_3, 
    'x_get_mtime__mutmut_4': x_get_mtime__mutmut_4, 
    'x_get_mtime__mutmut_5': x_get_mtime__mutmut_5, 
    'x_get_mtime__mutmut_6': x_get_mtime__mutmut_6, 
    'x_get_mtime__mutmut_7': x_get_mtime__mutmut_7, 
    'x_get_mtime__mutmut_8': x_get_mtime__mutmut_8, 
    'x_get_mtime__mutmut_9': x_get_mtime__mutmut_9, 
    'x_get_mtime__mutmut_10': x_get_mtime__mutmut_10, 
    'x_get_mtime__mutmut_11': x_get_mtime__mutmut_11, 
    'x_get_mtime__mutmut_12': x_get_mtime__mutmut_12, 
    'x_get_mtime__mutmut_13': x_get_mtime__mutmut_13
}

def get_mtime(*args, **kwargs):
    result = _mutmut_trampoline(x_get_mtime__mutmut_orig, x_get_mtime__mutmut_mutants, args, kwargs)
    return result 

get_mtime.__signature__ = _mutmut_signature(x_get_mtime__mutmut_orig)
x_get_mtime__mutmut_orig.__name__ = 'x_get_mtime'


def x_touch__mutmut_orig(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_1(
    path: Path | str,
    mode: int = 421,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_2(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = False,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_3(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = None

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_4(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(None)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_5(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() or not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_6(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_7(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(None)

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_8(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=None, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_9(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=None)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_10(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_11(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, )

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_12(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=False, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_13(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=False)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_14(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=None, exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_15(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=None)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_16(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(exist_ok=exist_ok)
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_17(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, )
    log.debug("Touched file", path=str(path))


def x_touch__mutmut_18(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug(None, path=str(path))


def x_touch__mutmut_19(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=None)


def x_touch__mutmut_20(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug(path=str(path))


def x_touch__mutmut_21(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", )


def x_touch__mutmut_22(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("XXTouched fileXX", path=str(path))


def x_touch__mutmut_23(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("touched file", path=str(path))


def x_touch__mutmut_24(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("TOUCHED FILE", path=str(path))


def x_touch__mutmut_25(
    path: Path | str,
    mode: int = 0o644,
    exist_ok: bool = True,
) -> None:
    """Create empty file or update timestamp.

    Args:
        path: File path
        mode: File permissions for new files
        exist_ok: If False, raise error if file exists

    Raises:
        FileExistsError: If exist_ok=False and file exists

    """
    path = Path(path)

    if path.exists() and not exist_ok:
        raise FileExistsError(f"File already exists: {path}")

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Touch the file
    path.touch(mode=mode, exist_ok=exist_ok)
    log.debug("Touched file", path=str(None))

x_touch__mutmut_mutants : ClassVar[MutantDict] = {
'x_touch__mutmut_1': x_touch__mutmut_1, 
    'x_touch__mutmut_2': x_touch__mutmut_2, 
    'x_touch__mutmut_3': x_touch__mutmut_3, 
    'x_touch__mutmut_4': x_touch__mutmut_4, 
    'x_touch__mutmut_5': x_touch__mutmut_5, 
    'x_touch__mutmut_6': x_touch__mutmut_6, 
    'x_touch__mutmut_7': x_touch__mutmut_7, 
    'x_touch__mutmut_8': x_touch__mutmut_8, 
    'x_touch__mutmut_9': x_touch__mutmut_9, 
    'x_touch__mutmut_10': x_touch__mutmut_10, 
    'x_touch__mutmut_11': x_touch__mutmut_11, 
    'x_touch__mutmut_12': x_touch__mutmut_12, 
    'x_touch__mutmut_13': x_touch__mutmut_13, 
    'x_touch__mutmut_14': x_touch__mutmut_14, 
    'x_touch__mutmut_15': x_touch__mutmut_15, 
    'x_touch__mutmut_16': x_touch__mutmut_16, 
    'x_touch__mutmut_17': x_touch__mutmut_17, 
    'x_touch__mutmut_18': x_touch__mutmut_18, 
    'x_touch__mutmut_19': x_touch__mutmut_19, 
    'x_touch__mutmut_20': x_touch__mutmut_20, 
    'x_touch__mutmut_21': x_touch__mutmut_21, 
    'x_touch__mutmut_22': x_touch__mutmut_22, 
    'x_touch__mutmut_23': x_touch__mutmut_23, 
    'x_touch__mutmut_24': x_touch__mutmut_24, 
    'x_touch__mutmut_25': x_touch__mutmut_25
}

def touch(*args, **kwargs):
    result = _mutmut_trampoline(x_touch__mutmut_orig, x_touch__mutmut_mutants, args, kwargs)
    return result 

touch.__signature__ = _mutmut_signature(x_touch__mutmut_orig)
x_touch__mutmut_orig.__name__ = 'x_touch'


def x_find_files__mutmut_orig(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_1(
    pattern: str,
    root: Path | str = "XX.XX",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_2(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = False,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_3(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = None

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_4(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(None)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_5(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_6(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning(None, root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_7(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=None)
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_8(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning(root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_9(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", )
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_10(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("XXSearch root doesn't existXX", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_11(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_12(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("SEARCH ROOT DOESN'T EXIST", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_13(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(None))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_14(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive or "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_15(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "XX**XX" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_16(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_17(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = None

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_18(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = None

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_19(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(None) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_20(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(None)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_21(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(None)

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_22(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(None))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_23(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip(None)))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_24(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.rstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_25(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("XX/XX")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_26(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = None

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_27(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug(None, pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_28(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=None, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_29(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=None, count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_30(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=None)
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_31(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug(pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_32(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_33(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_34(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), )
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_35(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("XXFound filesXX", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_36(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_37(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("FOUND FILES", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_38(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(None), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_39(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error(None, pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_40(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=None, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_41(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=None, error=str(e))
        return []


def x_find_files__mutmut_42(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=None)
        return []


def x_find_files__mutmut_43(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error(pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_44(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", root=str(root), error=str(e))
        return []


def x_find_files__mutmut_45(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, error=str(e))
        return []


def x_find_files__mutmut_46(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), )
        return []


def x_find_files__mutmut_47(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("XXFailed to find filesXX", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_48(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("failed to find files", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_49(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("FAILED TO FIND FILES", pattern=pattern, root=str(root), error=str(e))
        return []


def x_find_files__mutmut_50(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(None), error=str(e))
        return []


def x_find_files__mutmut_51(
    pattern: str,
    root: Path | str = ".",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching pattern.

    Args:
        pattern: Glob pattern (e.g., "*.py", "**/*.json")
        root: Root directory to search from
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    """
    root = Path(root)

    if not root.exists():
        log.warning("Search root doesn't exist", root=str(root))
        return []

    # Use glob or rglob based on recursive flag
    if recursive and "**" not in pattern:
        pattern = f"**/{pattern}"

    try:
        matches = list(root.glob(pattern)) if recursive else list(root.glob(pattern.lstrip("/")))

        # Filter to files only
        files = [p for p in matches if p.is_file()]

        log.debug("Found files", pattern=pattern, root=str(root), count=len(files))
        return files
    except Exception as e:
        log.error("Failed to find files", pattern=pattern, root=str(root), error=str(None))
        return []

x_find_files__mutmut_mutants : ClassVar[MutantDict] = {
'x_find_files__mutmut_1': x_find_files__mutmut_1, 
    'x_find_files__mutmut_2': x_find_files__mutmut_2, 
    'x_find_files__mutmut_3': x_find_files__mutmut_3, 
    'x_find_files__mutmut_4': x_find_files__mutmut_4, 
    'x_find_files__mutmut_5': x_find_files__mutmut_5, 
    'x_find_files__mutmut_6': x_find_files__mutmut_6, 
    'x_find_files__mutmut_7': x_find_files__mutmut_7, 
    'x_find_files__mutmut_8': x_find_files__mutmut_8, 
    'x_find_files__mutmut_9': x_find_files__mutmut_9, 
    'x_find_files__mutmut_10': x_find_files__mutmut_10, 
    'x_find_files__mutmut_11': x_find_files__mutmut_11, 
    'x_find_files__mutmut_12': x_find_files__mutmut_12, 
    'x_find_files__mutmut_13': x_find_files__mutmut_13, 
    'x_find_files__mutmut_14': x_find_files__mutmut_14, 
    'x_find_files__mutmut_15': x_find_files__mutmut_15, 
    'x_find_files__mutmut_16': x_find_files__mutmut_16, 
    'x_find_files__mutmut_17': x_find_files__mutmut_17, 
    'x_find_files__mutmut_18': x_find_files__mutmut_18, 
    'x_find_files__mutmut_19': x_find_files__mutmut_19, 
    'x_find_files__mutmut_20': x_find_files__mutmut_20, 
    'x_find_files__mutmut_21': x_find_files__mutmut_21, 
    'x_find_files__mutmut_22': x_find_files__mutmut_22, 
    'x_find_files__mutmut_23': x_find_files__mutmut_23, 
    'x_find_files__mutmut_24': x_find_files__mutmut_24, 
    'x_find_files__mutmut_25': x_find_files__mutmut_25, 
    'x_find_files__mutmut_26': x_find_files__mutmut_26, 
    'x_find_files__mutmut_27': x_find_files__mutmut_27, 
    'x_find_files__mutmut_28': x_find_files__mutmut_28, 
    'x_find_files__mutmut_29': x_find_files__mutmut_29, 
    'x_find_files__mutmut_30': x_find_files__mutmut_30, 
    'x_find_files__mutmut_31': x_find_files__mutmut_31, 
    'x_find_files__mutmut_32': x_find_files__mutmut_32, 
    'x_find_files__mutmut_33': x_find_files__mutmut_33, 
    'x_find_files__mutmut_34': x_find_files__mutmut_34, 
    'x_find_files__mutmut_35': x_find_files__mutmut_35, 
    'x_find_files__mutmut_36': x_find_files__mutmut_36, 
    'x_find_files__mutmut_37': x_find_files__mutmut_37, 
    'x_find_files__mutmut_38': x_find_files__mutmut_38, 
    'x_find_files__mutmut_39': x_find_files__mutmut_39, 
    'x_find_files__mutmut_40': x_find_files__mutmut_40, 
    'x_find_files__mutmut_41': x_find_files__mutmut_41, 
    'x_find_files__mutmut_42': x_find_files__mutmut_42, 
    'x_find_files__mutmut_43': x_find_files__mutmut_43, 
    'x_find_files__mutmut_44': x_find_files__mutmut_44, 
    'x_find_files__mutmut_45': x_find_files__mutmut_45, 
    'x_find_files__mutmut_46': x_find_files__mutmut_46, 
    'x_find_files__mutmut_47': x_find_files__mutmut_47, 
    'x_find_files__mutmut_48': x_find_files__mutmut_48, 
    'x_find_files__mutmut_49': x_find_files__mutmut_49, 
    'x_find_files__mutmut_50': x_find_files__mutmut_50, 
    'x_find_files__mutmut_51': x_find_files__mutmut_51
}

def find_files(*args, **kwargs):
    result = _mutmut_trampoline(x_find_files__mutmut_orig, x_find_files__mutmut_mutants, args, kwargs)
    return result 

find_files.__signature__ = _mutmut_signature(x_find_files__mutmut_orig)
x_find_files__mutmut_orig.__name__ = 'x_find_files'


def x_backup_file__mutmut_orig(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_1(
    path: Path | str,
    suffix: str = "XX.bakXX",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_2(
    path: Path | str,
    suffix: str = ".BAK",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_3(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = True,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_4(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = None

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_5(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(None)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_6(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_7(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug(None, path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_8(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=None)
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_9(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug(path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_10(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", )
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_11(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("XXSource file doesn't exist, no backup createdXX", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_12(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_13(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("SOURCE FILE DOESN'T EXIST, NO BACKUP CREATED", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_14(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(None))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_15(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = None
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_16(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime(None)
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_17(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("XX%Y%m%d_%H%M%SXX")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_18(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%y%m%d_%h%m%s")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_19(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%M%D_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_20(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = None
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_21(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(None)
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_22(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = None

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_23(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(None)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_24(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix - suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_25(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = None
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_26(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 2
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_27(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = None
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_28(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(None)
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_29(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter = 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_30(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter -= 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_31(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 2

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_32(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(None, str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_33(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), None)
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_34(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_35(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), )
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_36(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(None), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_37(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(None))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_38(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug(None, source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_39(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=None, backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_40(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=None)
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_41(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug(source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_42(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_43(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), )
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_44(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("XXCreated backupXX", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_45(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_46(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("CREATED BACKUP", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_47(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(None), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_48(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(None))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_49(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error(None, path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_50(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=None, error=str(e))
        return None


def x_backup_file__mutmut_51(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=None)
        return None


def x_backup_file__mutmut_52(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error(path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_53(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", error=str(e))
        return None


def x_backup_file__mutmut_54(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), )
        return None


def x_backup_file__mutmut_55(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("XXFailed to create backupXX", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_56(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("failed to create backup", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_57(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("FAILED TO CREATE BACKUP", path=str(path), error=str(e))
        return None


def x_backup_file__mutmut_58(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(None), error=str(e))
        return None


def x_backup_file__mutmut_59(
    path: Path | str,
    suffix: str = ".bak",
    timestamp: bool = False,
) -> Path | None:
    """Create backup copy of file.

    Args:
        path: File to backup
        suffix: Backup suffix
        timestamp: If True, add timestamp to backup name

    Returns:
        Path to backup file, or None if source doesn't exist

    """
    path = Path(path)

    if not path.exists():
        log.debug("Source file doesn't exist, no backup created", path=str(path))
        return None

    # Build backup filename
    if timestamp:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".{ts}{suffix}")
    else:
        backup_path = path.with_suffix(path.suffix + suffix)

        # Find unique name if backup already exists
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f"{path.suffix}{suffix}.{counter}")
            counter += 1

    try:
        shutil.copy2(str(path), str(backup_path))
        log.debug("Created backup", source=str(path), backup=str(backup_path))
        return backup_path
    except Exception as e:
        log.error("Failed to create backup", path=str(path), error=str(None))
        return None

x_backup_file__mutmut_mutants : ClassVar[MutantDict] = {
'x_backup_file__mutmut_1': x_backup_file__mutmut_1, 
    'x_backup_file__mutmut_2': x_backup_file__mutmut_2, 
    'x_backup_file__mutmut_3': x_backup_file__mutmut_3, 
    'x_backup_file__mutmut_4': x_backup_file__mutmut_4, 
    'x_backup_file__mutmut_5': x_backup_file__mutmut_5, 
    'x_backup_file__mutmut_6': x_backup_file__mutmut_6, 
    'x_backup_file__mutmut_7': x_backup_file__mutmut_7, 
    'x_backup_file__mutmut_8': x_backup_file__mutmut_8, 
    'x_backup_file__mutmut_9': x_backup_file__mutmut_9, 
    'x_backup_file__mutmut_10': x_backup_file__mutmut_10, 
    'x_backup_file__mutmut_11': x_backup_file__mutmut_11, 
    'x_backup_file__mutmut_12': x_backup_file__mutmut_12, 
    'x_backup_file__mutmut_13': x_backup_file__mutmut_13, 
    'x_backup_file__mutmut_14': x_backup_file__mutmut_14, 
    'x_backup_file__mutmut_15': x_backup_file__mutmut_15, 
    'x_backup_file__mutmut_16': x_backup_file__mutmut_16, 
    'x_backup_file__mutmut_17': x_backup_file__mutmut_17, 
    'x_backup_file__mutmut_18': x_backup_file__mutmut_18, 
    'x_backup_file__mutmut_19': x_backup_file__mutmut_19, 
    'x_backup_file__mutmut_20': x_backup_file__mutmut_20, 
    'x_backup_file__mutmut_21': x_backup_file__mutmut_21, 
    'x_backup_file__mutmut_22': x_backup_file__mutmut_22, 
    'x_backup_file__mutmut_23': x_backup_file__mutmut_23, 
    'x_backup_file__mutmut_24': x_backup_file__mutmut_24, 
    'x_backup_file__mutmut_25': x_backup_file__mutmut_25, 
    'x_backup_file__mutmut_26': x_backup_file__mutmut_26, 
    'x_backup_file__mutmut_27': x_backup_file__mutmut_27, 
    'x_backup_file__mutmut_28': x_backup_file__mutmut_28, 
    'x_backup_file__mutmut_29': x_backup_file__mutmut_29, 
    'x_backup_file__mutmut_30': x_backup_file__mutmut_30, 
    'x_backup_file__mutmut_31': x_backup_file__mutmut_31, 
    'x_backup_file__mutmut_32': x_backup_file__mutmut_32, 
    'x_backup_file__mutmut_33': x_backup_file__mutmut_33, 
    'x_backup_file__mutmut_34': x_backup_file__mutmut_34, 
    'x_backup_file__mutmut_35': x_backup_file__mutmut_35, 
    'x_backup_file__mutmut_36': x_backup_file__mutmut_36, 
    'x_backup_file__mutmut_37': x_backup_file__mutmut_37, 
    'x_backup_file__mutmut_38': x_backup_file__mutmut_38, 
    'x_backup_file__mutmut_39': x_backup_file__mutmut_39, 
    'x_backup_file__mutmut_40': x_backup_file__mutmut_40, 
    'x_backup_file__mutmut_41': x_backup_file__mutmut_41, 
    'x_backup_file__mutmut_42': x_backup_file__mutmut_42, 
    'x_backup_file__mutmut_43': x_backup_file__mutmut_43, 
    'x_backup_file__mutmut_44': x_backup_file__mutmut_44, 
    'x_backup_file__mutmut_45': x_backup_file__mutmut_45, 
    'x_backup_file__mutmut_46': x_backup_file__mutmut_46, 
    'x_backup_file__mutmut_47': x_backup_file__mutmut_47, 
    'x_backup_file__mutmut_48': x_backup_file__mutmut_48, 
    'x_backup_file__mutmut_49': x_backup_file__mutmut_49, 
    'x_backup_file__mutmut_50': x_backup_file__mutmut_50, 
    'x_backup_file__mutmut_51': x_backup_file__mutmut_51, 
    'x_backup_file__mutmut_52': x_backup_file__mutmut_52, 
    'x_backup_file__mutmut_53': x_backup_file__mutmut_53, 
    'x_backup_file__mutmut_54': x_backup_file__mutmut_54, 
    'x_backup_file__mutmut_55': x_backup_file__mutmut_55, 
    'x_backup_file__mutmut_56': x_backup_file__mutmut_56, 
    'x_backup_file__mutmut_57': x_backup_file__mutmut_57, 
    'x_backup_file__mutmut_58': x_backup_file__mutmut_58, 
    'x_backup_file__mutmut_59': x_backup_file__mutmut_59
}

def backup_file(*args, **kwargs):
    result = _mutmut_trampoline(x_backup_file__mutmut_orig, x_backup_file__mutmut_mutants, args, kwargs)
    return result 

backup_file.__signature__ = _mutmut_signature(x_backup_file__mutmut_orig)
x_backup_file__mutmut_orig.__name__ = 'x_backup_file'


__all__ = [
    "backup_file",
    "find_files",
    "get_mtime",
    "get_size",
    "touch",
]


# <3 🧱🤝📄🪄
