# provide/foundation/archive/xz.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import lzma
import shutil
from typing import BinaryIO

from attrs import define, validators

from provide.foundation.archive.base import BaseCompressor, _validate_compression_level
from provide.foundation.archive.defaults import DEFAULT_XZ_COMPRESSION_LEVEL
from provide.foundation.config.base import field

"""XZ/LZMA2 compression implementation using Python stdlib."""
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


@define(slots=True)
class XzCompressor(BaseCompressor):
    """XZ/LZMA2 compression implementation.

    Provides XZ compression and decompression using Python's stdlib lzma module.
    Does not handle bundling - use with TarArchive for .tar.xz files.

    XZ preset range: 0-9
    - 0: Fastest compression, lower ratio
    - 6: Default balanced setting
    - 9: Best compression, slower
    """

    level: int = field(
        default=DEFAULT_XZ_COMPRESSION_LEVEL,
        validator=validators.and_(validators.instance_of(int), _validate_compression_level),
    )

    @property
    def format_name(self) -> str:
        """Return the name of the compression format."""
        return "XZ"

    def _compress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream compression implementation."""
        with lzma.LZMAFile(output_stream, "wb", preset=self.level) as xz:
            shutil.copyfileobj(input_stream, xz)

    def _decompress_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Library-specific stream decompression implementation."""
        with lzma.LZMAFile(input_stream, "rb") as xz:
            shutil.copyfileobj(xz, output_stream)

    def _compress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes compression implementation."""
        return lzma.compress(data, preset=self.level)

    def _decompress_bytes_impl(self, data: bytes) -> bytes:
        """Library-specific bytes decompression implementation."""
        return lzma.decompress(data)


# <3 🧱🤝📦🪄
