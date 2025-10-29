# provide/foundation/streams/config.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from attrs import define

from provide.foundation.config.base import field
from provide.foundation.config.converters import parse_bool_extended
from provide.foundation.config.env import RuntimeConfig

"""Stream configuration for console output settings.

This module provides configuration for console stream behavior,
including color support and testing mode detection.
"""
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


@define(slots=True, repr=False)
class StreamConfig(RuntimeConfig):
    """Configuration for console stream output behavior."""

    no_color: bool = field(
        default=False,
        env_var="NO_COLOR",
        converter=parse_bool_extended,
        description="Disable color output in console",
    )

    force_color: bool = field(
        default=False,
        env_var="FORCE_COLOR",
        converter=parse_bool_extended,
        description="Force color output even when not in TTY",
    )

    click_testing: bool = field(
        default=False,
        env_var="CLICK_TESTING",
        converter=parse_bool_extended,
        description="Indicates if running inside Click testing framework",
    )

    force_stream_redirect: bool = field(
        default=False,
        env_var="FOUNDATION_FORCE_STREAM_REDIRECT",
        converter=parse_bool_extended,
        description="Force stream redirection in testing (bypasses Click testing guard)",
    )

    def supports_color(self) -> bool:
        """Determine if the console supports color output.

        Returns:
            True if color is supported, False otherwise

        """
        if self.no_color:
            return False

        if self.force_color:
            return True

        # Additional logic for TTY detection would go here
        # For now, just return based on the flags
        return not self.no_color


# Global instance for easy access
_stream_config: StreamConfig | None = None


def x_get_stream_config__mutmut_orig() -> StreamConfig:
    """Get the global stream configuration instance.

    Returns:
        StreamConfig instance loaded from environment

    """
    global _stream_config
    if _stream_config is None:
        _stream_config = StreamConfig.from_env()
    return _stream_config


def x_get_stream_config__mutmut_1() -> StreamConfig:
    """Get the global stream configuration instance.

    Returns:
        StreamConfig instance loaded from environment

    """
    global _stream_config
    if _stream_config is not None:
        _stream_config = StreamConfig.from_env()
    return _stream_config


def x_get_stream_config__mutmut_2() -> StreamConfig:
    """Get the global stream configuration instance.

    Returns:
        StreamConfig instance loaded from environment

    """
    global _stream_config
    if _stream_config is None:
        _stream_config = None
    return _stream_config


x_get_stream_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_stream_config__mutmut_1": x_get_stream_config__mutmut_1,
    "x_get_stream_config__mutmut_2": x_get_stream_config__mutmut_2,
}


def get_stream_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_stream_config__mutmut_orig, x_get_stream_config__mutmut_mutants, args, kwargs
    )
    return result


get_stream_config.__signature__ = _mutmut_signature(x_get_stream_config__mutmut_orig)
x_get_stream_config__mutmut_orig.__name__ = "x_get_stream_config"


def x_reset_stream_config__mutmut_orig() -> None:
    """Reset the global stream configuration (mainly for testing)."""
    global _stream_config
    _stream_config = None


def x_reset_stream_config__mutmut_1() -> None:
    """Reset the global stream configuration (mainly for testing)."""
    global _stream_config
    _stream_config = ""


x_reset_stream_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_reset_stream_config__mutmut_1": x_reset_stream_config__mutmut_1
}


def reset_stream_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_reset_stream_config__mutmut_orig, x_reset_stream_config__mutmut_mutants, args, kwargs
    )
    return result


reset_stream_config.__signature__ = _mutmut_signature(x_reset_stream_config__mutmut_orig)
x_reset_stream_config__mutmut_orig.__name__ = "x_reset_stream_config"


# <3 🧱🤝🌊🪄
