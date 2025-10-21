# provide/foundation/archive/types.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import IntEnum

"""Archive operation types and constants.

These constants are compatible with the PSPF/2025 format specification
used by flavorpack, allowing seamless integration between Foundation's
archive operations and PSPF package format operations.
"""
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


class ArchiveOperation(IntEnum):
    """Archive operation codes compatible with PSPF/2025 format.

    These operation codes match the PSPF/2025 v0 specification to ensure
    compatibility with flavorpack's package format. The hex values are
    canonical and must not be changed without updating the PSPF spec.

    Values:
        NONE: No operation (0x00)
        TAR: POSIX TAR archive bundling (0x01)
        GZIP: GZIP compression (0x10)
        BZIP2: BZIP2 compression (0x13)
        XZ: XZ/LZMA2 compression (0x16)
        ZSTD: Zstandard compression (0x1B)

    Example:
        >>> from provide.foundation.archive.types import ArchiveOperation
        >>> op = ArchiveOperation.TAR
        >>> assert op == 0x01
        >>> assert op.name == "TAR"

    """

    # Core operations
    NONE = 0x00  # No operation

    # Bundle operations (0x01-0x0F range)
    TAR = 0x01  # POSIX TAR archive (REQUIRED in PSPF v0)

    # Compression operations (0x10-0x2F range)
    GZIP = 0x10  # GZIP compression (REQUIRED in PSPF v0)
    BZIP2 = 0x13  # BZIP2 compression (REQUIRED in PSPF v0)
    XZ = 0x16  # XZ/LZMA2 compression (REQUIRED in PSPF v0)
    ZSTD = 0x1B  # Zstandard compression (REQUIRED in PSPF v0)

    # ZIP is not in PSPF v0, but we support it in Foundation
    # It uses a value outside the PSPF operation ranges
    ZIP = 0x30  # ZIP archive (Foundation extension)

    @classmethod
    def from_string(cls, name: str) -> ArchiveOperation:
        """Convert string operation name to enum.

        Args:
            name: Operation name (case-insensitive)

        Returns:
            ArchiveOperation enum value

        Raises:
            ValueError: If operation name is invalid

        Example:
            >>> ArchiveOperation.from_string("tar")
            <ArchiveOperation.TAR: 1>
            >>> ArchiveOperation.from_string("GZIP")
            <ArchiveOperation.GZIP: 16>

        """
        name_upper = name.upper()
        try:
            return cls[name_upper]
        except KeyError:
            raise ValueError(f"Unknown archive operation: {name}") from None

    def xǁArchiveOperationǁto_string__mutmut_orig(self) -> str:
        """Convert enum to lowercase string name.

        Returns:
            Lowercase operation name

        Example:
            >>> ArchiveOperation.TAR.to_string()
            'tar'

        """
        return self.name.lower()

    def xǁArchiveOperationǁto_string__mutmut_1(self) -> str:
        """Convert enum to lowercase string name.

        Returns:
            Lowercase operation name

        Example:
            >>> ArchiveOperation.TAR.to_string()
            'tar'

        """
        return self.name.upper()
    
    xǁArchiveOperationǁto_string__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁArchiveOperationǁto_string__mutmut_1': xǁArchiveOperationǁto_string__mutmut_1
    }
    
    def to_string(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁArchiveOperationǁto_string__mutmut_orig"), object.__getattribute__(self, "xǁArchiveOperationǁto_string__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_string.__signature__ = _mutmut_signature(xǁArchiveOperationǁto_string__mutmut_orig)
    xǁArchiveOperationǁto_string__mutmut_orig.__name__ = 'xǁArchiveOperationǁto_string'


# Inverse operations for extraction/decompression
INVERSE_OPERATIONS: dict[ArchiveOperation, str] = {
    ArchiveOperation.TAR: "untar",
    ArchiveOperation.GZIP: "gunzip",
    ArchiveOperation.BZIP2: "bunzip2",
    ArchiveOperation.XZ: "unxz",
    ArchiveOperation.ZSTD: "unzstd",
    ArchiveOperation.ZIP: "unzip",
}

# String operation name mapping (includes extraction aliases for convenience)
OPERATION_NAMES: dict[str, ArchiveOperation] = {
    "tar": ArchiveOperation.TAR,
    "untar": ArchiveOperation.TAR,
    "gzip": ArchiveOperation.GZIP,
    "gunzip": ArchiveOperation.GZIP,
    "bzip2": ArchiveOperation.BZIP2,
    "bunzip2": ArchiveOperation.BZIP2,
    "xz": ArchiveOperation.XZ,
    "unxz": ArchiveOperation.XZ,
    "zstd": ArchiveOperation.ZSTD,
    "unzstd": ArchiveOperation.ZSTD,
    "zip": ArchiveOperation.ZIP,
    "unzip": ArchiveOperation.ZIP,
}


def x_get_operation_from_string__mutmut_orig(op_string: str) -> ArchiveOperation:
    """Get operation enum from string (supports extraction aliases).

    Args:
        op_string: Operation string (e.g., "tar", "untar", "gzip", "gunzip")

    Returns:
        ArchiveOperation enum value

    Raises:
        ValueError: If operation string is invalid

    Example:
        >>> get_operation_from_string("tar")
        <ArchiveOperation.TAR: 1>
        >>> get_operation_from_string("untar")  # Same as "tar"
        <ArchiveOperation.TAR: 1>

    """
    op_lower = op_string.lower()
    if op_lower not in OPERATION_NAMES:
        raise ValueError(f"Unknown archive operation: {op_string}")
    return OPERATION_NAMES[op_lower]


def x_get_operation_from_string__mutmut_1(op_string: str) -> ArchiveOperation:
    """Get operation enum from string (supports extraction aliases).

    Args:
        op_string: Operation string (e.g., "tar", "untar", "gzip", "gunzip")

    Returns:
        ArchiveOperation enum value

    Raises:
        ValueError: If operation string is invalid

    Example:
        >>> get_operation_from_string("tar")
        <ArchiveOperation.TAR: 1>
        >>> get_operation_from_string("untar")  # Same as "tar"
        <ArchiveOperation.TAR: 1>

    """
    op_lower = None
    if op_lower not in OPERATION_NAMES:
        raise ValueError(f"Unknown archive operation: {op_string}")
    return OPERATION_NAMES[op_lower]


def x_get_operation_from_string__mutmut_2(op_string: str) -> ArchiveOperation:
    """Get operation enum from string (supports extraction aliases).

    Args:
        op_string: Operation string (e.g., "tar", "untar", "gzip", "gunzip")

    Returns:
        ArchiveOperation enum value

    Raises:
        ValueError: If operation string is invalid

    Example:
        >>> get_operation_from_string("tar")
        <ArchiveOperation.TAR: 1>
        >>> get_operation_from_string("untar")  # Same as "tar"
        <ArchiveOperation.TAR: 1>

    """
    op_lower = op_string.upper()
    if op_lower not in OPERATION_NAMES:
        raise ValueError(f"Unknown archive operation: {op_string}")
    return OPERATION_NAMES[op_lower]


def x_get_operation_from_string__mutmut_3(op_string: str) -> ArchiveOperation:
    """Get operation enum from string (supports extraction aliases).

    Args:
        op_string: Operation string (e.g., "tar", "untar", "gzip", "gunzip")

    Returns:
        ArchiveOperation enum value

    Raises:
        ValueError: If operation string is invalid

    Example:
        >>> get_operation_from_string("tar")
        <ArchiveOperation.TAR: 1>
        >>> get_operation_from_string("untar")  # Same as "tar"
        <ArchiveOperation.TAR: 1>

    """
    op_lower = op_string.lower()
    if op_lower in OPERATION_NAMES:
        raise ValueError(f"Unknown archive operation: {op_string}")
    return OPERATION_NAMES[op_lower]


def x_get_operation_from_string__mutmut_4(op_string: str) -> ArchiveOperation:
    """Get operation enum from string (supports extraction aliases).

    Args:
        op_string: Operation string (e.g., "tar", "untar", "gzip", "gunzip")

    Returns:
        ArchiveOperation enum value

    Raises:
        ValueError: If operation string is invalid

    Example:
        >>> get_operation_from_string("tar")
        <ArchiveOperation.TAR: 1>
        >>> get_operation_from_string("untar")  # Same as "tar"
        <ArchiveOperation.TAR: 1>

    """
    op_lower = op_string.lower()
    if op_lower not in OPERATION_NAMES:
        raise ValueError(None)
    return OPERATION_NAMES[op_lower]

x_get_operation_from_string__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_operation_from_string__mutmut_1': x_get_operation_from_string__mutmut_1, 
    'x_get_operation_from_string__mutmut_2': x_get_operation_from_string__mutmut_2, 
    'x_get_operation_from_string__mutmut_3': x_get_operation_from_string__mutmut_3, 
    'x_get_operation_from_string__mutmut_4': x_get_operation_from_string__mutmut_4
}

def get_operation_from_string(*args, **kwargs):
    result = _mutmut_trampoline(x_get_operation_from_string__mutmut_orig, x_get_operation_from_string__mutmut_mutants, args, kwargs)
    return result 

get_operation_from_string.__signature__ = _mutmut_signature(x_get_operation_from_string__mutmut_orig)
x_get_operation_from_string__mutmut_orig.__name__ = 'x_get_operation_from_string'


__all__ = [
    "INVERSE_OPERATIONS",
    "OPERATION_NAMES",
    "ArchiveOperation",
    "get_operation_from_string",
]


# <3 🧱🤝📦🪄
