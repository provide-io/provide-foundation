# provide/foundation/file/directory.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
import shutil

from provide.foundation.errors.decorators import resilient
from provide.foundation.logger import get_logger

"""Directory operations and utilities."""

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


def x_ensure_dir__mutmut_orig(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_1(
    path: Path | str,
    mode: int = 494,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_2(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = False,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_3(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = None

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_4(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(None)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_5(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_6(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=None, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_7(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=None, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_8(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=None)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_9(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_10(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_11(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, )
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_12(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=False)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_13(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug(None, path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_14(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=None, mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_15(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=None)
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_16(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug(path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_17(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_18(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), )
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_19(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("XXCreated directoryXX", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_20(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_21(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("CREATED DIRECTORY", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_22(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(None), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_23(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(None))
    elif not path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_24(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif path.is_dir():
        raise NotADirectoryError(f"Path exists but is not a directory: {path}")

    return path


def x_ensure_dir__mutmut_25(
    path: Path | str,
    mode: int = 0o755,
    parents: bool = True,
) -> Path:
    """Ensure directory exists with proper permissions.

    Args:
        path: Directory path
        mode: Directory permissions
        parents: Create parent directories if needed

    Returns:
        Path object for the directory

    """
    path = Path(path)

    if not path.exists():
        path.mkdir(mode=mode, parents=parents, exist_ok=True)
        log.debug("Created directory", path=str(path), mode=oct(mode))
    elif not path.is_dir():
        raise NotADirectoryError(None)

    return path

x_ensure_dir__mutmut_mutants : ClassVar[MutantDict] = {
'x_ensure_dir__mutmut_1': x_ensure_dir__mutmut_1, 
    'x_ensure_dir__mutmut_2': x_ensure_dir__mutmut_2, 
    'x_ensure_dir__mutmut_3': x_ensure_dir__mutmut_3, 
    'x_ensure_dir__mutmut_4': x_ensure_dir__mutmut_4, 
    'x_ensure_dir__mutmut_5': x_ensure_dir__mutmut_5, 
    'x_ensure_dir__mutmut_6': x_ensure_dir__mutmut_6, 
    'x_ensure_dir__mutmut_7': x_ensure_dir__mutmut_7, 
    'x_ensure_dir__mutmut_8': x_ensure_dir__mutmut_8, 
    'x_ensure_dir__mutmut_9': x_ensure_dir__mutmut_9, 
    'x_ensure_dir__mutmut_10': x_ensure_dir__mutmut_10, 
    'x_ensure_dir__mutmut_11': x_ensure_dir__mutmut_11, 
    'x_ensure_dir__mutmut_12': x_ensure_dir__mutmut_12, 
    'x_ensure_dir__mutmut_13': x_ensure_dir__mutmut_13, 
    'x_ensure_dir__mutmut_14': x_ensure_dir__mutmut_14, 
    'x_ensure_dir__mutmut_15': x_ensure_dir__mutmut_15, 
    'x_ensure_dir__mutmut_16': x_ensure_dir__mutmut_16, 
    'x_ensure_dir__mutmut_17': x_ensure_dir__mutmut_17, 
    'x_ensure_dir__mutmut_18': x_ensure_dir__mutmut_18, 
    'x_ensure_dir__mutmut_19': x_ensure_dir__mutmut_19, 
    'x_ensure_dir__mutmut_20': x_ensure_dir__mutmut_20, 
    'x_ensure_dir__mutmut_21': x_ensure_dir__mutmut_21, 
    'x_ensure_dir__mutmut_22': x_ensure_dir__mutmut_22, 
    'x_ensure_dir__mutmut_23': x_ensure_dir__mutmut_23, 
    'x_ensure_dir__mutmut_24': x_ensure_dir__mutmut_24, 
    'x_ensure_dir__mutmut_25': x_ensure_dir__mutmut_25
}

def ensure_dir(*args, **kwargs):
    result = _mutmut_trampoline(x_ensure_dir__mutmut_orig, x_ensure_dir__mutmut_mutants, args, kwargs)
    return result 

ensure_dir.__signature__ = _mutmut_signature(x_ensure_dir__mutmut_orig)
x_ensure_dir__mutmut_orig.__name__ = 'x_ensure_dir'


def x_ensure_parent_dir__mutmut_orig(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_1(
    file_path: Path | str,
    mode: int = 494,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_2(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = None
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_3(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(None)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_4(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = None

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_5(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent or parent != Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_6(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent == Path():
        return ensure_dir(parent, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_7(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(None, mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_8(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=None, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_9(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=None)

    return parent


def x_ensure_parent_dir__mutmut_10(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(mode=mode, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_11(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, parents=True)

    return parent


def x_ensure_parent_dir__mutmut_12(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, )

    return parent


def x_ensure_parent_dir__mutmut_13(
    file_path: Path | str,
    mode: int = 0o755,
) -> Path:
    """Ensure parent directory of file exists.

    Args:
        file_path: File path whose parent to ensure
        mode: Directory permissions

    Returns:
        Path object for the parent directory

    """
    file_path = Path(file_path)
    parent = file_path.parent

    if parent and parent != Path():
        return ensure_dir(parent, mode=mode, parents=False)

    return parent

x_ensure_parent_dir__mutmut_mutants : ClassVar[MutantDict] = {
'x_ensure_parent_dir__mutmut_1': x_ensure_parent_dir__mutmut_1, 
    'x_ensure_parent_dir__mutmut_2': x_ensure_parent_dir__mutmut_2, 
    'x_ensure_parent_dir__mutmut_3': x_ensure_parent_dir__mutmut_3, 
    'x_ensure_parent_dir__mutmut_4': x_ensure_parent_dir__mutmut_4, 
    'x_ensure_parent_dir__mutmut_5': x_ensure_parent_dir__mutmut_5, 
    'x_ensure_parent_dir__mutmut_6': x_ensure_parent_dir__mutmut_6, 
    'x_ensure_parent_dir__mutmut_7': x_ensure_parent_dir__mutmut_7, 
    'x_ensure_parent_dir__mutmut_8': x_ensure_parent_dir__mutmut_8, 
    'x_ensure_parent_dir__mutmut_9': x_ensure_parent_dir__mutmut_9, 
    'x_ensure_parent_dir__mutmut_10': x_ensure_parent_dir__mutmut_10, 
    'x_ensure_parent_dir__mutmut_11': x_ensure_parent_dir__mutmut_11, 
    'x_ensure_parent_dir__mutmut_12': x_ensure_parent_dir__mutmut_12, 
    'x_ensure_parent_dir__mutmut_13': x_ensure_parent_dir__mutmut_13
}

def ensure_parent_dir(*args, **kwargs):
    result = _mutmut_trampoline(x_ensure_parent_dir__mutmut_orig, x_ensure_parent_dir__mutmut_mutants, args, kwargs)
    return result 

ensure_parent_dir.__signature__ = _mutmut_signature(x_ensure_parent_dir__mutmut_orig)
x_ensure_parent_dir__mutmut_orig.__name__ = 'x_ensure_parent_dir'


@resilient(fallback=False, suppress=(FileNotFoundError,) if False else ())
def safe_rmtree(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Remove directory tree safely.

    Args:
        path: Directory to remove
        missing_ok: If True, don't raise error if doesn't exist

    Returns:
        True if removed, False if didn't exist

    Raises:
        OSError: If removal fails and directory exists

    """
    path = Path(path)

    if path.exists():
        shutil.rmtree(path)
        log.debug("Removed directory tree", path=str(path))
        return True
    if missing_ok:
        log.debug("Directory already absent", path=str(path))
        return False
    raise FileNotFoundError(f"Directory does not exist: {path}")


__all__ = [
    "ensure_dir",
    "ensure_parent_dir",
    "safe_rmtree",
]


# <3 🧱🤝📄🪄
