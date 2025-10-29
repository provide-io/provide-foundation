# provide/foundation/archive/zstd.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import shutil
from typing import Any, BinaryIO

from attrs import Attribute, define, validators

from provide.foundation.archive.base import BaseCompressor
from provide.foundation.archive.defaults import DEFAULT_ZSTD_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""Zstandard compression implementation (requires zstandard package)."""
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


def x__validate_zstd_level__mutmut_orig(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 <= value <= 22):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_1(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if 1 <= value <= 22:
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_2(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (2 <= value <= 22):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_3(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 < value <= 22):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_4(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 <= value < 22):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_5(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 <= value <= 23):
        raise ValueError(f"ZSTD compression level must be between 1 and 22, got {value}")


def x__validate_zstd_level__mutmut_6(instance: Any, attribute: Attribute[int], value: int) -> None:
    """Validate ZSTD compression level (1-22)."""
    if not (1 <= value <= 22):
        raise ValueError(None)


x__validate_zstd_level__mutmut_mutants: ClassVar[MutantDict] = {
    "x__validate_zstd_level__mutmut_1": x__validate_zstd_level__mutmut_1,
    "x__validate_zstd_level__mutmut_2": x__validate_zstd_level__mutmut_2,
    "x__validate_zstd_level__mutmut_3": x__validate_zstd_level__mutmut_3,
    "x__validate_zstd_level__mutmut_4": x__validate_zstd_level__mutmut_4,
    "x__validate_zstd_level__mutmut_5": x__validate_zstd_level__mutmut_5,
    "x__validate_zstd_level__mutmut_6": x__validate_zstd_level__mutmut_6,
}


def _validate_zstd_level(*args, **kwargs):
    result = _mutmut_trampoline(
        x__validate_zstd_level__mutmut_orig, x__validate_zstd_level__mutmut_mutants, args, kwargs
    )
    return result


_validate_zstd_level.__signature__ = _mutmut_signature(x__validate_zstd_level__mutmut_orig)
x__validate_zstd_level__mutmut_orig.__name__ = "x__validate_zstd_level"


@define(slots=True)
class ZstdCompressor(BaseCompressor):
    """Zstandard compression implementation.

    Provides ZSTD compression and decompression using the zstandard package.
    Does not handle bundling - use with TarArchive for .tar.zst files.

    ZSTD level range: 1-22
    - 1: Fastest compression, lower ratio
    - 3: Default balanced setting
    - 22: Best compression, much slower

    Note: Requires the 'zstandard' package to be installed.
          Install with: pip install provide-foundation[compression]
    """

    level: int = field(
        default=DEFAULT_ZSTD_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_zstd_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "ZSTD"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD compression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        cctx = zstd.ZstdCompressor(level=self.level)
        with cctx.stream_writer(output_stream) as compressor:
            shutil.copyfileobj(input_stream, compressor)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD decompression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(input_stream) as decompressor:
            shutil.copyfileobj(decompressor, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD compression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        cctx = zstd.ZstdCompressor(level=self.level)
        return cctx.compress(data)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        try:
            import zstandard as zstd
        except ImportError as e:
            raise ImportError(
                "ZSTD decompression requires 'zstandard' package. "
                "Install with: pip install provide-foundation[compression]"
            ) from e

        dctx = zstd.ZstdDecompressor()
        return dctx.decompress(data)


# <3 🧱🤝📦🪄
