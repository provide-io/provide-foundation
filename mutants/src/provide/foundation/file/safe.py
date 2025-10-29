# provide/foundation/file/safe.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
import shutil

"""Safe file operations with error handling and defaults."""

_logger = None
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


def x_safe_read__mutmut_orig(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_1(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = None

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_2(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(None)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_3(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = None
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_4(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(None)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_5(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(None, path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_6(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=None)
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_7(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_8(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(
            "File not found, returning default",
        )
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_9(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("XXFile not found, returning defaultXX", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_10(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("file not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_11(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("FILE NOT FOUND, RETURNING DEFAULT", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_12(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(None))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_13(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None or encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_14(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_15(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(None) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_16(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning(None, path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_17(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=None, error=str(e))
        return default


def x_safe_read__mutmut_18(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=None)
        return default


def x_safe_read__mutmut_19(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning(path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_20(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", error=str(e))
        return default


def x_safe_read__mutmut_21(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning(
            "Failed to read file",
            path=str(path),
        )
        return default


def x_safe_read__mutmut_22(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("XXFailed to read fileXX", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_23(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("failed to read file", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_24(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("FAILED TO READ FILE", path=str(path), error=str(e))
        return default


def x_safe_read__mutmut_25(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(None), error=str(e))
        return default


def x_safe_read__mutmut_26(
    path: Path | str,
    default: bytes | None = None,
    encoding: str | None = None,
) -> bytes | str | None:
    """Read file safely, returning default if not found.

    Args:
        path: File to read
        default: Value to return if file doesn't exist
        encoding: If provided, decode bytes to str

    Returns:
        File contents or default value

    """
    path = Path(path)

    try:
        data = path.read_bytes()
        if encoding:
            return data.decode(encoding)
        return data
    except FileNotFoundError:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("File not found, returning default", path=str(path))
        if default is not None and encoding:
            return default.decode(encoding) if isinstance(default, bytes) else default
        return default
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().warning("Failed to read file", path=str(path), error=str(None))
        return default


x_safe_read__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_read__mutmut_1": x_safe_read__mutmut_1,
    "x_safe_read__mutmut_2": x_safe_read__mutmut_2,
    "x_safe_read__mutmut_3": x_safe_read__mutmut_3,
    "x_safe_read__mutmut_4": x_safe_read__mutmut_4,
    "x_safe_read__mutmut_5": x_safe_read__mutmut_5,
    "x_safe_read__mutmut_6": x_safe_read__mutmut_6,
    "x_safe_read__mutmut_7": x_safe_read__mutmut_7,
    "x_safe_read__mutmut_8": x_safe_read__mutmut_8,
    "x_safe_read__mutmut_9": x_safe_read__mutmut_9,
    "x_safe_read__mutmut_10": x_safe_read__mutmut_10,
    "x_safe_read__mutmut_11": x_safe_read__mutmut_11,
    "x_safe_read__mutmut_12": x_safe_read__mutmut_12,
    "x_safe_read__mutmut_13": x_safe_read__mutmut_13,
    "x_safe_read__mutmut_14": x_safe_read__mutmut_14,
    "x_safe_read__mutmut_15": x_safe_read__mutmut_15,
    "x_safe_read__mutmut_16": x_safe_read__mutmut_16,
    "x_safe_read__mutmut_17": x_safe_read__mutmut_17,
    "x_safe_read__mutmut_18": x_safe_read__mutmut_18,
    "x_safe_read__mutmut_19": x_safe_read__mutmut_19,
    "x_safe_read__mutmut_20": x_safe_read__mutmut_20,
    "x_safe_read__mutmut_21": x_safe_read__mutmut_21,
    "x_safe_read__mutmut_22": x_safe_read__mutmut_22,
    "x_safe_read__mutmut_23": x_safe_read__mutmut_23,
    "x_safe_read__mutmut_24": x_safe_read__mutmut_24,
    "x_safe_read__mutmut_25": x_safe_read__mutmut_25,
    "x_safe_read__mutmut_26": x_safe_read__mutmut_26,
}


def safe_read(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_read__mutmut_orig, x_safe_read__mutmut_mutants, args, kwargs)
    return result


safe_read.__signature__ = _mutmut_signature(x_safe_read__mutmut_orig)
x_safe_read__mutmut_orig.__name__ = "x_safe_read"


def x_safe_read_text__mutmut_orig(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_1(
    path: Path | str,
    default: str = "XXXX",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_2(
    path: Path | str,
    default: str = "",
    encoding: str = "XXutf-8XX",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_3(
    path: Path | str,
    default: str = "",
    encoding: str = "UTF-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_4(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = None
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_5(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(None, default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_6(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=None, encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_7(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(encoding), encoding=None)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_8(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(default=default.encode(encoding), encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_9(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, encoding=encoding)
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_10(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(
        path,
        default=default.encode(encoding),
    )
    return result if isinstance(result, str) else default


def x_safe_read_text__mutmut_11(
    path: Path | str,
    default: str = "",
    encoding: str = "utf-8",
) -> str:
    """Read text file safely with default.

    Args:
        path: File to read
        default: Default text if file doesn't exist
        encoding: Text encoding

    Returns:
        File contents or default text

    """
    result = safe_read(path, default=default.encode(None), encoding=encoding)
    return result if isinstance(result, str) else default


x_safe_read_text__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_read_text__mutmut_1": x_safe_read_text__mutmut_1,
    "x_safe_read_text__mutmut_2": x_safe_read_text__mutmut_2,
    "x_safe_read_text__mutmut_3": x_safe_read_text__mutmut_3,
    "x_safe_read_text__mutmut_4": x_safe_read_text__mutmut_4,
    "x_safe_read_text__mutmut_5": x_safe_read_text__mutmut_5,
    "x_safe_read_text__mutmut_6": x_safe_read_text__mutmut_6,
    "x_safe_read_text__mutmut_7": x_safe_read_text__mutmut_7,
    "x_safe_read_text__mutmut_8": x_safe_read_text__mutmut_8,
    "x_safe_read_text__mutmut_9": x_safe_read_text__mutmut_9,
    "x_safe_read_text__mutmut_10": x_safe_read_text__mutmut_10,
    "x_safe_read_text__mutmut_11": x_safe_read_text__mutmut_11,
}


def safe_read_text(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_read_text__mutmut_orig, x_safe_read_text__mutmut_mutants, args, kwargs)
    return result


safe_read_text.__signature__ = _mutmut_signature(x_safe_read_text__mutmut_orig)
x_safe_read_text__mutmut_orig.__name__ = "x_safe_read_text"


def x_safe_delete__mutmut_orig(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_1(
    path: Path | str,
    missing_ok: bool = False,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_2(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = None

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_3(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(None)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_4(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(None, path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_5(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=None)
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_6(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_7(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(
            "Deleted file",
        )
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_8(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("XXDeleted fileXX", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_9(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_10(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("DELETED FILE", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_11(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(None))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_12(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return False
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_13(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug(None, path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_14(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=None)
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_15(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug(path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_16(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug(
                "File already absent",
            )
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_17(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("XXFile already absentXX", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_18(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("file already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_19(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("FILE ALREADY ABSENT", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_20(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(None))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_21(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return True
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_22(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(None, path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_23(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=None, error=str(e))
        raise


def x_safe_delete__mutmut_24(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=None)
        raise


def x_safe_delete__mutmut_25(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_26(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", error=str(e))
        raise


def x_safe_delete__mutmut_27(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            "Failed to delete file",
            path=str(path),
        )
        raise


def x_safe_delete__mutmut_28(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("XXFailed to delete fileXX", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_29(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("failed to delete file", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_30(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("FAILED TO DELETE FILE", path=str(path), error=str(e))
        raise


def x_safe_delete__mutmut_31(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(None), error=str(e))
        raise


def x_safe_delete__mutmut_32(
    path: Path | str,
    missing_ok: bool = True,
) -> bool:
    """Delete file safely.

    Args:
        path: File to delete
        missing_ok: If True, don't raise error if file doesn't exist

    Returns:
        True if deleted, False if didn't exist

    Raises:
        OSError: If deletion fails and file exists

    """
    path = Path(path)

    try:
        path.unlink()
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Deleted file", path=str(path))
        return True
    except FileNotFoundError:
        if missing_ok:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().debug("File already absent", path=str(path))
            return False
        raise
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to delete file", path=str(path), error=str(None))
        raise


x_safe_delete__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_delete__mutmut_1": x_safe_delete__mutmut_1,
    "x_safe_delete__mutmut_2": x_safe_delete__mutmut_2,
    "x_safe_delete__mutmut_3": x_safe_delete__mutmut_3,
    "x_safe_delete__mutmut_4": x_safe_delete__mutmut_4,
    "x_safe_delete__mutmut_5": x_safe_delete__mutmut_5,
    "x_safe_delete__mutmut_6": x_safe_delete__mutmut_6,
    "x_safe_delete__mutmut_7": x_safe_delete__mutmut_7,
    "x_safe_delete__mutmut_8": x_safe_delete__mutmut_8,
    "x_safe_delete__mutmut_9": x_safe_delete__mutmut_9,
    "x_safe_delete__mutmut_10": x_safe_delete__mutmut_10,
    "x_safe_delete__mutmut_11": x_safe_delete__mutmut_11,
    "x_safe_delete__mutmut_12": x_safe_delete__mutmut_12,
    "x_safe_delete__mutmut_13": x_safe_delete__mutmut_13,
    "x_safe_delete__mutmut_14": x_safe_delete__mutmut_14,
    "x_safe_delete__mutmut_15": x_safe_delete__mutmut_15,
    "x_safe_delete__mutmut_16": x_safe_delete__mutmut_16,
    "x_safe_delete__mutmut_17": x_safe_delete__mutmut_17,
    "x_safe_delete__mutmut_18": x_safe_delete__mutmut_18,
    "x_safe_delete__mutmut_19": x_safe_delete__mutmut_19,
    "x_safe_delete__mutmut_20": x_safe_delete__mutmut_20,
    "x_safe_delete__mutmut_21": x_safe_delete__mutmut_21,
    "x_safe_delete__mutmut_22": x_safe_delete__mutmut_22,
    "x_safe_delete__mutmut_23": x_safe_delete__mutmut_23,
    "x_safe_delete__mutmut_24": x_safe_delete__mutmut_24,
    "x_safe_delete__mutmut_25": x_safe_delete__mutmut_25,
    "x_safe_delete__mutmut_26": x_safe_delete__mutmut_26,
    "x_safe_delete__mutmut_27": x_safe_delete__mutmut_27,
    "x_safe_delete__mutmut_28": x_safe_delete__mutmut_28,
    "x_safe_delete__mutmut_29": x_safe_delete__mutmut_29,
    "x_safe_delete__mutmut_30": x_safe_delete__mutmut_30,
    "x_safe_delete__mutmut_31": x_safe_delete__mutmut_31,
    "x_safe_delete__mutmut_32": x_safe_delete__mutmut_32,
}


def safe_delete(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_delete__mutmut_orig, x_safe_delete__mutmut_mutants, args, kwargs)
    return result


safe_delete.__signature__ = _mutmut_signature(x_safe_delete__mutmut_orig)
x_safe_delete__mutmut_orig.__name__ = "x_safe_delete"


def x_safe_move__mutmut_orig(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_1(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = True,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_2(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = None
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_3(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(None)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_4(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = None

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_5(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(None)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_6(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_7(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(None)

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_8(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() or not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_9(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_10(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(None)

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_11(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=None, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_12(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=None)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_13(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_14(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(
        parents=True,
    )

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_15(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=False, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_16(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=False)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_17(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(None, str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_18(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), None)
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_19(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_20(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(
            str(src),
        )
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_21(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(None), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_22(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(None))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_23(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(None, src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_24(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=None, dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_25(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=None)
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_26(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_27(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_28(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(
            "Moved file",
            src=str(src),
        )
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_29(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("XXMoved fileXX", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_30(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_31(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("MOVED FILE", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_32(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(None), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_33(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(None))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_34(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(None, src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_35(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=None, dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_36(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=None, error=str(e))
        raise


def x_safe_move__mutmut_37(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=None)
        raise


def x_safe_move__mutmut_38(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_39(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_40(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), error=str(e))
        raise


def x_safe_move__mutmut_41(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            "Failed to move file",
            src=str(src),
            dst=str(dst),
        )
        raise


def x_safe_move__mutmut_42(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("XXFailed to move fileXX", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_43(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("failed to move file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_44(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("FAILED TO MOVE FILE", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_45(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(None), dst=str(dst), error=str(e))
        raise


def x_safe_move__mutmut_46(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(None), error=str(e))
        raise


def x_safe_move__mutmut_47(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
) -> None:
    """Move file safely with optional overwrite.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If move operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Moved file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to move file", src=str(src), dst=str(dst), error=str(None))
        raise


x_safe_move__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_move__mutmut_1": x_safe_move__mutmut_1,
    "x_safe_move__mutmut_2": x_safe_move__mutmut_2,
    "x_safe_move__mutmut_3": x_safe_move__mutmut_3,
    "x_safe_move__mutmut_4": x_safe_move__mutmut_4,
    "x_safe_move__mutmut_5": x_safe_move__mutmut_5,
    "x_safe_move__mutmut_6": x_safe_move__mutmut_6,
    "x_safe_move__mutmut_7": x_safe_move__mutmut_7,
    "x_safe_move__mutmut_8": x_safe_move__mutmut_8,
    "x_safe_move__mutmut_9": x_safe_move__mutmut_9,
    "x_safe_move__mutmut_10": x_safe_move__mutmut_10,
    "x_safe_move__mutmut_11": x_safe_move__mutmut_11,
    "x_safe_move__mutmut_12": x_safe_move__mutmut_12,
    "x_safe_move__mutmut_13": x_safe_move__mutmut_13,
    "x_safe_move__mutmut_14": x_safe_move__mutmut_14,
    "x_safe_move__mutmut_15": x_safe_move__mutmut_15,
    "x_safe_move__mutmut_16": x_safe_move__mutmut_16,
    "x_safe_move__mutmut_17": x_safe_move__mutmut_17,
    "x_safe_move__mutmut_18": x_safe_move__mutmut_18,
    "x_safe_move__mutmut_19": x_safe_move__mutmut_19,
    "x_safe_move__mutmut_20": x_safe_move__mutmut_20,
    "x_safe_move__mutmut_21": x_safe_move__mutmut_21,
    "x_safe_move__mutmut_22": x_safe_move__mutmut_22,
    "x_safe_move__mutmut_23": x_safe_move__mutmut_23,
    "x_safe_move__mutmut_24": x_safe_move__mutmut_24,
    "x_safe_move__mutmut_25": x_safe_move__mutmut_25,
    "x_safe_move__mutmut_26": x_safe_move__mutmut_26,
    "x_safe_move__mutmut_27": x_safe_move__mutmut_27,
    "x_safe_move__mutmut_28": x_safe_move__mutmut_28,
    "x_safe_move__mutmut_29": x_safe_move__mutmut_29,
    "x_safe_move__mutmut_30": x_safe_move__mutmut_30,
    "x_safe_move__mutmut_31": x_safe_move__mutmut_31,
    "x_safe_move__mutmut_32": x_safe_move__mutmut_32,
    "x_safe_move__mutmut_33": x_safe_move__mutmut_33,
    "x_safe_move__mutmut_34": x_safe_move__mutmut_34,
    "x_safe_move__mutmut_35": x_safe_move__mutmut_35,
    "x_safe_move__mutmut_36": x_safe_move__mutmut_36,
    "x_safe_move__mutmut_37": x_safe_move__mutmut_37,
    "x_safe_move__mutmut_38": x_safe_move__mutmut_38,
    "x_safe_move__mutmut_39": x_safe_move__mutmut_39,
    "x_safe_move__mutmut_40": x_safe_move__mutmut_40,
    "x_safe_move__mutmut_41": x_safe_move__mutmut_41,
    "x_safe_move__mutmut_42": x_safe_move__mutmut_42,
    "x_safe_move__mutmut_43": x_safe_move__mutmut_43,
    "x_safe_move__mutmut_44": x_safe_move__mutmut_44,
    "x_safe_move__mutmut_45": x_safe_move__mutmut_45,
    "x_safe_move__mutmut_46": x_safe_move__mutmut_46,
    "x_safe_move__mutmut_47": x_safe_move__mutmut_47,
}


def safe_move(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_move__mutmut_orig, x_safe_move__mutmut_mutants, args, kwargs)
    return result


safe_move.__signature__ = _mutmut_signature(x_safe_move__mutmut_orig)
x_safe_move__mutmut_orig.__name__ = "x_safe_move"


def x_safe_copy__mutmut_orig(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_1(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = True,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_2(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = False,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_3(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = None
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_4(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(None)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_5(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = None

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_6(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(None)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_7(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_8(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(None)

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_9(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() or not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_10(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_11(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(None)

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_12(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=None, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_13(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=None)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_14(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_15(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(
        parents=True,
    )

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_16(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=False, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_17(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=False)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_18(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(None, str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_19(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), None)
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_20(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_21(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(
                str(src),
            )
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_22(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(None), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_23(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(None))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_24(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(None, str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_25(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), None)
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_26(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_27(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(
                str(src),
            )
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_28(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(None), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_29(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(None))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_30(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(None, src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_31(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=None, dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_32(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=None)
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_33(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_34(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_35(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug(
            "Copied file",
            src=str(src),
        )
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_36(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("XXCopied fileXX", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_37(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_38(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("COPIED FILE", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_39(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(None), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_40(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(None))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_41(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(None, src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_42(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=None, dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_43(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=None, error=str(e))
        raise


def x_safe_copy__mutmut_44(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=None)
        raise


def x_safe_copy__mutmut_45(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_46(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_47(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), error=str(e))
        raise


def x_safe_copy__mutmut_48(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            "Failed to copy file",
            src=str(src),
            dst=str(dst),
        )
        raise


def x_safe_copy__mutmut_49(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("XXFailed to copy fileXX", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_50(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("failed to copy file", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_51(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("FAILED TO COPY FILE", src=str(src), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_52(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(None), dst=str(dst), error=str(e))
        raise


def x_safe_copy__mutmut_53(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(None), error=str(e))
        raise


def x_safe_copy__mutmut_54(
    src: Path | str,
    dst: Path | str,
    overwrite: bool = False,
    preserve_mode: bool = True,
) -> None:
    """Copy file safely with metadata preservation.

    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite existing destination
        preserve_mode: Whether to preserve file permissions

    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails

    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dst}")

    # Ensure destination directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if preserve_mode:
            shutil.copy2(str(src), str(dst))
        else:
            shutil.copy(str(src), str(dst))
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().debug("Copied file", src=str(src), dst=str(dst))
    except Exception as e:
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error("Failed to copy file", src=str(src), dst=str(dst), error=str(None))
        raise


x_safe_copy__mutmut_mutants: ClassVar[MutantDict] = {
    "x_safe_copy__mutmut_1": x_safe_copy__mutmut_1,
    "x_safe_copy__mutmut_2": x_safe_copy__mutmut_2,
    "x_safe_copy__mutmut_3": x_safe_copy__mutmut_3,
    "x_safe_copy__mutmut_4": x_safe_copy__mutmut_4,
    "x_safe_copy__mutmut_5": x_safe_copy__mutmut_5,
    "x_safe_copy__mutmut_6": x_safe_copy__mutmut_6,
    "x_safe_copy__mutmut_7": x_safe_copy__mutmut_7,
    "x_safe_copy__mutmut_8": x_safe_copy__mutmut_8,
    "x_safe_copy__mutmut_9": x_safe_copy__mutmut_9,
    "x_safe_copy__mutmut_10": x_safe_copy__mutmut_10,
    "x_safe_copy__mutmut_11": x_safe_copy__mutmut_11,
    "x_safe_copy__mutmut_12": x_safe_copy__mutmut_12,
    "x_safe_copy__mutmut_13": x_safe_copy__mutmut_13,
    "x_safe_copy__mutmut_14": x_safe_copy__mutmut_14,
    "x_safe_copy__mutmut_15": x_safe_copy__mutmut_15,
    "x_safe_copy__mutmut_16": x_safe_copy__mutmut_16,
    "x_safe_copy__mutmut_17": x_safe_copy__mutmut_17,
    "x_safe_copy__mutmut_18": x_safe_copy__mutmut_18,
    "x_safe_copy__mutmut_19": x_safe_copy__mutmut_19,
    "x_safe_copy__mutmut_20": x_safe_copy__mutmut_20,
    "x_safe_copy__mutmut_21": x_safe_copy__mutmut_21,
    "x_safe_copy__mutmut_22": x_safe_copy__mutmut_22,
    "x_safe_copy__mutmut_23": x_safe_copy__mutmut_23,
    "x_safe_copy__mutmut_24": x_safe_copy__mutmut_24,
    "x_safe_copy__mutmut_25": x_safe_copy__mutmut_25,
    "x_safe_copy__mutmut_26": x_safe_copy__mutmut_26,
    "x_safe_copy__mutmut_27": x_safe_copy__mutmut_27,
    "x_safe_copy__mutmut_28": x_safe_copy__mutmut_28,
    "x_safe_copy__mutmut_29": x_safe_copy__mutmut_29,
    "x_safe_copy__mutmut_30": x_safe_copy__mutmut_30,
    "x_safe_copy__mutmut_31": x_safe_copy__mutmut_31,
    "x_safe_copy__mutmut_32": x_safe_copy__mutmut_32,
    "x_safe_copy__mutmut_33": x_safe_copy__mutmut_33,
    "x_safe_copy__mutmut_34": x_safe_copy__mutmut_34,
    "x_safe_copy__mutmut_35": x_safe_copy__mutmut_35,
    "x_safe_copy__mutmut_36": x_safe_copy__mutmut_36,
    "x_safe_copy__mutmut_37": x_safe_copy__mutmut_37,
    "x_safe_copy__mutmut_38": x_safe_copy__mutmut_38,
    "x_safe_copy__mutmut_39": x_safe_copy__mutmut_39,
    "x_safe_copy__mutmut_40": x_safe_copy__mutmut_40,
    "x_safe_copy__mutmut_41": x_safe_copy__mutmut_41,
    "x_safe_copy__mutmut_42": x_safe_copy__mutmut_42,
    "x_safe_copy__mutmut_43": x_safe_copy__mutmut_43,
    "x_safe_copy__mutmut_44": x_safe_copy__mutmut_44,
    "x_safe_copy__mutmut_45": x_safe_copy__mutmut_45,
    "x_safe_copy__mutmut_46": x_safe_copy__mutmut_46,
    "x_safe_copy__mutmut_47": x_safe_copy__mutmut_47,
    "x_safe_copy__mutmut_48": x_safe_copy__mutmut_48,
    "x_safe_copy__mutmut_49": x_safe_copy__mutmut_49,
    "x_safe_copy__mutmut_50": x_safe_copy__mutmut_50,
    "x_safe_copy__mutmut_51": x_safe_copy__mutmut_51,
    "x_safe_copy__mutmut_52": x_safe_copy__mutmut_52,
    "x_safe_copy__mutmut_53": x_safe_copy__mutmut_53,
    "x_safe_copy__mutmut_54": x_safe_copy__mutmut_54,
}


def safe_copy(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_copy__mutmut_orig, x_safe_copy__mutmut_mutants, args, kwargs)
    return result


safe_copy.__signature__ = _mutmut_signature(x_safe_copy__mutmut_orig)
x_safe_copy__mutmut_orig.__name__ = "x_safe_copy"


__all__ = [
    "safe_copy",
    "safe_delete",
    "safe_move",
    "safe_read",
    "safe_read_text",
]


# <3 🧱🤝📄🪄
