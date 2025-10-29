# provide/foundation/file/atomic.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import contextlib
import os
from pathlib import Path

from provide.foundation.logger import get_logger

"""Atomic file operations using temp file + rename pattern."""

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


def x_atomic_write__mutmut_orig(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_1(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = True,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_2(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = False,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_3(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = None

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_4(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(None)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_5(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup or path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_6(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = None
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_7(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(None)
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_8(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix - ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_9(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + "XX.bakXX")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_10(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".BAK")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_11(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(None)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_12(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug(None, backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_13(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=None)
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_14(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug(backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_15(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug(
                "Created backup",
            )
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_16(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("XXCreated backupXX", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_17(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_18(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("CREATED BACKUP", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_19(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(None))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_20(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning(None, error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_21(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=None)

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_22(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning(error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_23(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning(
                "Failed to create backup",
            )

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_24(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("XXFailed to create backupXX", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_25(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_26(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("FAILED TO CREATE BACKUP", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_27(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(None))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_28(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=None, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_29(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=None)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_30(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_31(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(
        parents=True,
    )

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_32(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=False, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_33(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=False)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_34(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = ""
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_35(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_36(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = None
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_37(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode or path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_38(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(None):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_39(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = None

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_40(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is not None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_41(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = None
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_42(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 439
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_43(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = None
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_44(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(None)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_45(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(1)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_46(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(None)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_47(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = None

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_48(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode | ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_49(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_50(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = None

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_51(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=None,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_52(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=None,
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_53(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=None,
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_54(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_55(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_56(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_57(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix="XX.tmpXX",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_58(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".TMP",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_59(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(None, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_60(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, None)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_61(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_62(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(
            temp_fd,
        )

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_63(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(None, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_64(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, None) as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_65(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen("wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_66(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(
            temp_fd,
        ) as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_67(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "XXwbXX") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_68(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "WB") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_69(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(None)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_70(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(None)

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_71(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(None)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_72(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(None).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_73(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            None,
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_74(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=None,
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_75(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=None,
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_76(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_77(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_78(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_79(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_80(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_81(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "XXAtomically wrote fileXX",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_82(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_83(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "ATOMICALLY WROTE FILE",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_84(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(None),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_85(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(None) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_86(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            None,
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_87(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=None,
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_88(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=None,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_89(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=None,
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_90(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_91(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_92(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_93(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_94(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "XXAtomic write failed, cleaning up temp fileXX",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_95(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_96(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "ATOMIC WRITE FAILED, CLEANING UP TEMP FILE",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_97(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(None),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_98(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(None),
        )
        with contextlib.suppress(OSError):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_99(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(None):
            Path(temp_path).unlink()
        raise


def x_atomic_write__mutmut_100(
    path: Path | str,
    data: bytes,
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write file atomically using temp file + rename.

    This ensures that the file is either fully written or not written at all,
    preventing partial writes or corruption.

    Args:
        path: Target file path
        data: Binary data to write
        mode: Optional file permissions (e.g., 0o644)
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails

    """
    path = Path(path)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        try:
            path.rename(backup_path)
            log.debug("Created backup", backup=str(backup_path))
        except OSError as e:
            log.warning("Failed to create backup", error=str(e))

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determine final permissions before creating file (avoid race condition)
    final_mode = None
    if mode is not None:
        final_mode = mode
    elif preserve_mode and path.exists():
        # Get existing permissions
        with contextlib.suppress(OSError):
            final_mode = path.stat().st_mode

    if final_mode is None:
        # Default permissions (respecting umask)
        default_mode = 0o666
        current_umask = os.umask(0)
        os.umask(current_umask)
        final_mode = default_mode & ~current_umask

    # Create temp file with final permissions in a single operation (no race)
    # Use os.open() instead of secure_temp_file for atomic permission setting
    import tempfile

    temp_fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )

    try:
        # Set permissions immediately on the file descriptor (atomic)
        os.fchmod(temp_fd, final_mode)

        # Write data
        with os.fdopen(temp_fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        Path(temp_path).replace(path)

        log.debug(
            "Atomically wrote file",
            path=str(path),
            size=len(data),
            mode=oct(mode) if mode else None,
        )
    except (OSError, PermissionError) as e:
        # Clean up temp file on error
        log.error(
            "Atomic write failed, cleaning up temp file",
            path=str(path),
            temp_path=temp_path,
            error=str(e),
        )
        with contextlib.suppress(OSError):
            Path(None).unlink()
        raise


x_atomic_write__mutmut_mutants: ClassVar[MutantDict] = {
    "x_atomic_write__mutmut_1": x_atomic_write__mutmut_1,
    "x_atomic_write__mutmut_2": x_atomic_write__mutmut_2,
    "x_atomic_write__mutmut_3": x_atomic_write__mutmut_3,
    "x_atomic_write__mutmut_4": x_atomic_write__mutmut_4,
    "x_atomic_write__mutmut_5": x_atomic_write__mutmut_5,
    "x_atomic_write__mutmut_6": x_atomic_write__mutmut_6,
    "x_atomic_write__mutmut_7": x_atomic_write__mutmut_7,
    "x_atomic_write__mutmut_8": x_atomic_write__mutmut_8,
    "x_atomic_write__mutmut_9": x_atomic_write__mutmut_9,
    "x_atomic_write__mutmut_10": x_atomic_write__mutmut_10,
    "x_atomic_write__mutmut_11": x_atomic_write__mutmut_11,
    "x_atomic_write__mutmut_12": x_atomic_write__mutmut_12,
    "x_atomic_write__mutmut_13": x_atomic_write__mutmut_13,
    "x_atomic_write__mutmut_14": x_atomic_write__mutmut_14,
    "x_atomic_write__mutmut_15": x_atomic_write__mutmut_15,
    "x_atomic_write__mutmut_16": x_atomic_write__mutmut_16,
    "x_atomic_write__mutmut_17": x_atomic_write__mutmut_17,
    "x_atomic_write__mutmut_18": x_atomic_write__mutmut_18,
    "x_atomic_write__mutmut_19": x_atomic_write__mutmut_19,
    "x_atomic_write__mutmut_20": x_atomic_write__mutmut_20,
    "x_atomic_write__mutmut_21": x_atomic_write__mutmut_21,
    "x_atomic_write__mutmut_22": x_atomic_write__mutmut_22,
    "x_atomic_write__mutmut_23": x_atomic_write__mutmut_23,
    "x_atomic_write__mutmut_24": x_atomic_write__mutmut_24,
    "x_atomic_write__mutmut_25": x_atomic_write__mutmut_25,
    "x_atomic_write__mutmut_26": x_atomic_write__mutmut_26,
    "x_atomic_write__mutmut_27": x_atomic_write__mutmut_27,
    "x_atomic_write__mutmut_28": x_atomic_write__mutmut_28,
    "x_atomic_write__mutmut_29": x_atomic_write__mutmut_29,
    "x_atomic_write__mutmut_30": x_atomic_write__mutmut_30,
    "x_atomic_write__mutmut_31": x_atomic_write__mutmut_31,
    "x_atomic_write__mutmut_32": x_atomic_write__mutmut_32,
    "x_atomic_write__mutmut_33": x_atomic_write__mutmut_33,
    "x_atomic_write__mutmut_34": x_atomic_write__mutmut_34,
    "x_atomic_write__mutmut_35": x_atomic_write__mutmut_35,
    "x_atomic_write__mutmut_36": x_atomic_write__mutmut_36,
    "x_atomic_write__mutmut_37": x_atomic_write__mutmut_37,
    "x_atomic_write__mutmut_38": x_atomic_write__mutmut_38,
    "x_atomic_write__mutmut_39": x_atomic_write__mutmut_39,
    "x_atomic_write__mutmut_40": x_atomic_write__mutmut_40,
    "x_atomic_write__mutmut_41": x_atomic_write__mutmut_41,
    "x_atomic_write__mutmut_42": x_atomic_write__mutmut_42,
    "x_atomic_write__mutmut_43": x_atomic_write__mutmut_43,
    "x_atomic_write__mutmut_44": x_atomic_write__mutmut_44,
    "x_atomic_write__mutmut_45": x_atomic_write__mutmut_45,
    "x_atomic_write__mutmut_46": x_atomic_write__mutmut_46,
    "x_atomic_write__mutmut_47": x_atomic_write__mutmut_47,
    "x_atomic_write__mutmut_48": x_atomic_write__mutmut_48,
    "x_atomic_write__mutmut_49": x_atomic_write__mutmut_49,
    "x_atomic_write__mutmut_50": x_atomic_write__mutmut_50,
    "x_atomic_write__mutmut_51": x_atomic_write__mutmut_51,
    "x_atomic_write__mutmut_52": x_atomic_write__mutmut_52,
    "x_atomic_write__mutmut_53": x_atomic_write__mutmut_53,
    "x_atomic_write__mutmut_54": x_atomic_write__mutmut_54,
    "x_atomic_write__mutmut_55": x_atomic_write__mutmut_55,
    "x_atomic_write__mutmut_56": x_atomic_write__mutmut_56,
    "x_atomic_write__mutmut_57": x_atomic_write__mutmut_57,
    "x_atomic_write__mutmut_58": x_atomic_write__mutmut_58,
    "x_atomic_write__mutmut_59": x_atomic_write__mutmut_59,
    "x_atomic_write__mutmut_60": x_atomic_write__mutmut_60,
    "x_atomic_write__mutmut_61": x_atomic_write__mutmut_61,
    "x_atomic_write__mutmut_62": x_atomic_write__mutmut_62,
    "x_atomic_write__mutmut_63": x_atomic_write__mutmut_63,
    "x_atomic_write__mutmut_64": x_atomic_write__mutmut_64,
    "x_atomic_write__mutmut_65": x_atomic_write__mutmut_65,
    "x_atomic_write__mutmut_66": x_atomic_write__mutmut_66,
    "x_atomic_write__mutmut_67": x_atomic_write__mutmut_67,
    "x_atomic_write__mutmut_68": x_atomic_write__mutmut_68,
    "x_atomic_write__mutmut_69": x_atomic_write__mutmut_69,
    "x_atomic_write__mutmut_70": x_atomic_write__mutmut_70,
    "x_atomic_write__mutmut_71": x_atomic_write__mutmut_71,
    "x_atomic_write__mutmut_72": x_atomic_write__mutmut_72,
    "x_atomic_write__mutmut_73": x_atomic_write__mutmut_73,
    "x_atomic_write__mutmut_74": x_atomic_write__mutmut_74,
    "x_atomic_write__mutmut_75": x_atomic_write__mutmut_75,
    "x_atomic_write__mutmut_76": x_atomic_write__mutmut_76,
    "x_atomic_write__mutmut_77": x_atomic_write__mutmut_77,
    "x_atomic_write__mutmut_78": x_atomic_write__mutmut_78,
    "x_atomic_write__mutmut_79": x_atomic_write__mutmut_79,
    "x_atomic_write__mutmut_80": x_atomic_write__mutmut_80,
    "x_atomic_write__mutmut_81": x_atomic_write__mutmut_81,
    "x_atomic_write__mutmut_82": x_atomic_write__mutmut_82,
    "x_atomic_write__mutmut_83": x_atomic_write__mutmut_83,
    "x_atomic_write__mutmut_84": x_atomic_write__mutmut_84,
    "x_atomic_write__mutmut_85": x_atomic_write__mutmut_85,
    "x_atomic_write__mutmut_86": x_atomic_write__mutmut_86,
    "x_atomic_write__mutmut_87": x_atomic_write__mutmut_87,
    "x_atomic_write__mutmut_88": x_atomic_write__mutmut_88,
    "x_atomic_write__mutmut_89": x_atomic_write__mutmut_89,
    "x_atomic_write__mutmut_90": x_atomic_write__mutmut_90,
    "x_atomic_write__mutmut_91": x_atomic_write__mutmut_91,
    "x_atomic_write__mutmut_92": x_atomic_write__mutmut_92,
    "x_atomic_write__mutmut_93": x_atomic_write__mutmut_93,
    "x_atomic_write__mutmut_94": x_atomic_write__mutmut_94,
    "x_atomic_write__mutmut_95": x_atomic_write__mutmut_95,
    "x_atomic_write__mutmut_96": x_atomic_write__mutmut_96,
    "x_atomic_write__mutmut_97": x_atomic_write__mutmut_97,
    "x_atomic_write__mutmut_98": x_atomic_write__mutmut_98,
    "x_atomic_write__mutmut_99": x_atomic_write__mutmut_99,
    "x_atomic_write__mutmut_100": x_atomic_write__mutmut_100,
}


def atomic_write(*args, **kwargs):
    result = _mutmut_trampoline(x_atomic_write__mutmut_orig, x_atomic_write__mutmut_mutants, args, kwargs)
    return result


atomic_write.__signature__ = _mutmut_signature(x_atomic_write__mutmut_orig)
x_atomic_write__mutmut_orig.__name__ = "x_atomic_write"


def x_atomic_write_text__mutmut_orig(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_1(
    path: Path | str,
    text: str,
    encoding: str = "XXutf-8XX",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_2(
    path: Path | str,
    text: str,
    encoding: str = "UTF-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_3(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = True,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_4(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = False,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_5(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = None
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_6(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(None)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_7(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(None, data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_8(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, None, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_9(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=None, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_10(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=None, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_11(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, backup=backup, preserve_mode=None)


def x_atomic_write_text__mutmut_12(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(data, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_13(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, mode=mode, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_14(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, backup=backup, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_15(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(path, data, mode=mode, preserve_mode=preserve_mode)


def x_atomic_write_text__mutmut_16(
    path: Path | str,
    text: str,
    encoding: str = "utf-8",
    mode: int | None = None,
    backup: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Write text file atomically.

    Args:
        path: Target file path
        text: Text content to write
        encoding: Text encoding (default: utf-8)
        mode: Optional file permissions
        backup: Create .bak file before overwrite
        preserve_mode: Whether to preserve existing file permissions when mode is None

    Raises:
        OSError: If file operation fails
        UnicodeEncodeError: If text cannot be encoded

    """
    data = text.encode(encoding)
    atomic_write(
        path,
        data,
        mode=mode,
        backup=backup,
    )


x_atomic_write_text__mutmut_mutants: ClassVar[MutantDict] = {
    "x_atomic_write_text__mutmut_1": x_atomic_write_text__mutmut_1,
    "x_atomic_write_text__mutmut_2": x_atomic_write_text__mutmut_2,
    "x_atomic_write_text__mutmut_3": x_atomic_write_text__mutmut_3,
    "x_atomic_write_text__mutmut_4": x_atomic_write_text__mutmut_4,
    "x_atomic_write_text__mutmut_5": x_atomic_write_text__mutmut_5,
    "x_atomic_write_text__mutmut_6": x_atomic_write_text__mutmut_6,
    "x_atomic_write_text__mutmut_7": x_atomic_write_text__mutmut_7,
    "x_atomic_write_text__mutmut_8": x_atomic_write_text__mutmut_8,
    "x_atomic_write_text__mutmut_9": x_atomic_write_text__mutmut_9,
    "x_atomic_write_text__mutmut_10": x_atomic_write_text__mutmut_10,
    "x_atomic_write_text__mutmut_11": x_atomic_write_text__mutmut_11,
    "x_atomic_write_text__mutmut_12": x_atomic_write_text__mutmut_12,
    "x_atomic_write_text__mutmut_13": x_atomic_write_text__mutmut_13,
    "x_atomic_write_text__mutmut_14": x_atomic_write_text__mutmut_14,
    "x_atomic_write_text__mutmut_15": x_atomic_write_text__mutmut_15,
    "x_atomic_write_text__mutmut_16": x_atomic_write_text__mutmut_16,
}


def atomic_write_text(*args, **kwargs):
    result = _mutmut_trampoline(
        x_atomic_write_text__mutmut_orig, x_atomic_write_text__mutmut_mutants, args, kwargs
    )
    return result


atomic_write_text.__signature__ = _mutmut_signature(x_atomic_write_text__mutmut_orig)
x_atomic_write_text__mutmut_orig.__name__ = "x_atomic_write_text"


def x_atomic_replace__mutmut_orig(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_1(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = False,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_2(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = None

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_3(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(None)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_4(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_5(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(None)

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_6(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = ""
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_7(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(None):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_8(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = None

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_9(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(None, data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_10(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, None, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_11(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=None, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_12(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=None, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_13(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=False, preserve_mode=None)


def x_atomic_replace__mutmut_14(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(data, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_15(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, mode=mode, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_16(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, backup=False, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_17(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, preserve_mode=preserve_mode)


def x_atomic_replace__mutmut_18(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(
        path,
        data,
        mode=mode,
        backup=False,
    )


def x_atomic_replace__mutmut_19(
    path: Path | str,
    data: bytes,
    preserve_mode: bool = True,
) -> None:
    """Replace existing file atomically, preserving permissions.

    Args:
        path: Target file path (must exist)
        data: Binary data to write
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If file operation fails

    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    mode = None
    if preserve_mode:
        with contextlib.suppress(OSError):
            mode = path.stat().st_mode

    # When preserve_mode is False, we explicitly pass preserve_mode=False to atomic_write
    # and let it handle the non-preservation (atomic_write won't preserve even if file exists)
    atomic_write(path, data, mode=mode, backup=True, preserve_mode=preserve_mode)


x_atomic_replace__mutmut_mutants: ClassVar[MutantDict] = {
    "x_atomic_replace__mutmut_1": x_atomic_replace__mutmut_1,
    "x_atomic_replace__mutmut_2": x_atomic_replace__mutmut_2,
    "x_atomic_replace__mutmut_3": x_atomic_replace__mutmut_3,
    "x_atomic_replace__mutmut_4": x_atomic_replace__mutmut_4,
    "x_atomic_replace__mutmut_5": x_atomic_replace__mutmut_5,
    "x_atomic_replace__mutmut_6": x_atomic_replace__mutmut_6,
    "x_atomic_replace__mutmut_7": x_atomic_replace__mutmut_7,
    "x_atomic_replace__mutmut_8": x_atomic_replace__mutmut_8,
    "x_atomic_replace__mutmut_9": x_atomic_replace__mutmut_9,
    "x_atomic_replace__mutmut_10": x_atomic_replace__mutmut_10,
    "x_atomic_replace__mutmut_11": x_atomic_replace__mutmut_11,
    "x_atomic_replace__mutmut_12": x_atomic_replace__mutmut_12,
    "x_atomic_replace__mutmut_13": x_atomic_replace__mutmut_13,
    "x_atomic_replace__mutmut_14": x_atomic_replace__mutmut_14,
    "x_atomic_replace__mutmut_15": x_atomic_replace__mutmut_15,
    "x_atomic_replace__mutmut_16": x_atomic_replace__mutmut_16,
    "x_atomic_replace__mutmut_17": x_atomic_replace__mutmut_17,
    "x_atomic_replace__mutmut_18": x_atomic_replace__mutmut_18,
    "x_atomic_replace__mutmut_19": x_atomic_replace__mutmut_19,
}


def atomic_replace(*args, **kwargs):
    result = _mutmut_trampoline(x_atomic_replace__mutmut_orig, x_atomic_replace__mutmut_mutants, args, kwargs)
    return result


atomic_replace.__signature__ = _mutmut_signature(x_atomic_replace__mutmut_orig)
x_atomic_replace__mutmut_orig.__name__ = "x_atomic_replace"


__all__ = [
    "atomic_replace",
    "atomic_write",
    "atomic_write_text",
]


# <3 🧱🤝📄🪄
