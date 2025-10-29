# provide/foundation/utils/versioning.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
import threading

"""Shared version discovery logic for provide-io packages.

This module provides thread-safe version discovery with caching,
supporting VERSION files, package metadata, and development fallbacks.
"""

# Thread-safe lazy initialization state
_version_lock = threading.Lock()
_cached_versions: dict[str, str] = {}
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


def x_reset_version_cache__mutmut_orig(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(package_name, None)


def x_reset_version_cache__mutmut_1(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is not None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(package_name, None)


def x_reset_version_cache__mutmut_2(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(None, None)


def x_reset_version_cache__mutmut_3(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(None)


def x_reset_version_cache__mutmut_4(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(
                package_name,
            )


x_reset_version_cache__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_version_cache__mutmut_1": x_reset_version_cache__mutmut_1,
    "x_reset_version_cache__mutmut_2": x_reset_version_cache__mutmut_2,
    "x_reset_version_cache__mutmut_3": x_reset_version_cache__mutmut_3,
    "x_reset_version_cache__mutmut_4": x_reset_version_cache__mutmut_4,
}


def reset_version_cache(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_version_cache__mutmut_orig, x_reset_version_cache__mutmut_mutants, args, kwargs
    )
    return result


reset_version_cache.__signature__ = _mutmut_signature(x_reset_version_cache__mutmut_orig)
x_reset_version_cache__mutmut_orig.__name__ = "x_reset_version_cache"


def x__find_project_root__mutmut_orig(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_1(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = None

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_2(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current == current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_3(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = None
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_4(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current * "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_5(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "XXVERSIONXX"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_6(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "version"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_7(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = None

    return None


x__find_project_root__mutmut_mutants: ClassVar[MutantDict] = {
    "x__find_project_root__mutmut_1": x__find_project_root__mutmut_1,
    "x__find_project_root__mutmut_2": x__find_project_root__mutmut_2,
    "x__find_project_root__mutmut_3": x__find_project_root__mutmut_3,
    "x__find_project_root__mutmut_4": x__find_project_root__mutmut_4,
    "x__find_project_root__mutmut_5": x__find_project_root__mutmut_5,
    "x__find_project_root__mutmut_6": x__find_project_root__mutmut_6,
    "x__find_project_root__mutmut_7": x__find_project_root__mutmut_7,
}


def _find_project_root(*args, **kwargs):
    result = _mutmut_trampoline(
        x__find_project_root__mutmut_orig, x__find_project_root__mutmut_mutants, args, kwargs
    )
    return result


_find_project_root.__signature__ = _mutmut_signature(x__find_project_root__mutmut_orig)
x__find_project_root__mutmut_orig.__name__ = "x__find_project_root"


def x_get_version__mutmut_orig(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_1(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name not in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_2(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name not in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_3(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_4(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = None
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_5(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(None).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_6(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = None
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_7(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame or frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_8(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = None
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_9(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = None
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_10(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(None).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_11(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = None

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_12(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = None
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_13(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(None)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_14(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = None
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_15(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root * "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_16(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "XXVERSIONXX"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_17(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "version"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_18(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = None
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_19(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = None
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_20(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = None
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_21(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(None)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_22(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = None
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_23(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = None
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_24(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "XX0.0.0-devXX"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_25(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-DEV"
        _cached_versions[package_name] = version_str
        return version_str


def x_get_version__mutmut_26(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = None
        return version_str


x_get_version__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_version__mutmut_1": x_get_version__mutmut_1,
    "x_get_version__mutmut_2": x_get_version__mutmut_2,
    "x_get_version__mutmut_3": x_get_version__mutmut_3,
    "x_get_version__mutmut_4": x_get_version__mutmut_4,
    "x_get_version__mutmut_5": x_get_version__mutmut_5,
    "x_get_version__mutmut_6": x_get_version__mutmut_6,
    "x_get_version__mutmut_7": x_get_version__mutmut_7,
    "x_get_version__mutmut_8": x_get_version__mutmut_8,
    "x_get_version__mutmut_9": x_get_version__mutmut_9,
    "x_get_version__mutmut_10": x_get_version__mutmut_10,
    "x_get_version__mutmut_11": x_get_version__mutmut_11,
    "x_get_version__mutmut_12": x_get_version__mutmut_12,
    "x_get_version__mutmut_13": x_get_version__mutmut_13,
    "x_get_version__mutmut_14": x_get_version__mutmut_14,
    "x_get_version__mutmut_15": x_get_version__mutmut_15,
    "x_get_version__mutmut_16": x_get_version__mutmut_16,
    "x_get_version__mutmut_17": x_get_version__mutmut_17,
    "x_get_version__mutmut_18": x_get_version__mutmut_18,
    "x_get_version__mutmut_19": x_get_version__mutmut_19,
    "x_get_version__mutmut_20": x_get_version__mutmut_20,
    "x_get_version__mutmut_21": x_get_version__mutmut_21,
    "x_get_version__mutmut_22": x_get_version__mutmut_22,
    "x_get_version__mutmut_23": x_get_version__mutmut_23,
    "x_get_version__mutmut_24": x_get_version__mutmut_24,
    "x_get_version__mutmut_25": x_get_version__mutmut_25,
    "x_get_version__mutmut_26": x_get_version__mutmut_26,
}


def get_version(*args, **kwargs):
    result = _mutmut_trampoline(x_get_version__mutmut_orig, x_get_version__mutmut_mutants, args, kwargs)
    return result


get_version.__signature__ = _mutmut_signature(x_get_version__mutmut_orig)
x_get_version__mutmut_orig.__name__ = "x_get_version"


__all__ = [
    "_find_project_root",
    "get_version",
    "reset_version_cache",
]


# <3 🧱🤝🧰🪄
