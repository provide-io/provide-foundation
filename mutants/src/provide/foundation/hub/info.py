# provide/foundation/hub/info.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Command information and metadata structures."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from provide.foundation.hub.introspection import ParameterInfo

from attrs import define, field

__all__ = ["CommandInfo"]
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


@define(frozen=True, slots=True)
class CommandInfo:
    """Framework-agnostic command information.

    Stores metadata about a registered command without framework-specific
    dependencies. The parameters field contains introspected parameter
    information that can be used by any CLI adapter.

    Attributes:
        name: Command name
        func: Command function/callable
        description: Command description (help text)
        aliases: Alternative names for the command
        hidden: Whether command is hidden from help
        category: Command category for organization
        metadata: Additional custom metadata
        parent: Parent command path (for nested commands)
        parameters: Introspected parameter information (lazy-loaded)

    """

    name: str
    func: Callable[..., Any]
    description: str | None = None
    aliases: list[str] = field(factory=list)
    hidden: bool = False
    category: str | None = None
    metadata: dict[str, Any] = field(factory=dict)
    parent: str | None = None  # Parent path extracted from dot notation
    parameters: list[ParameterInfo] | None = None


# <3 🧱🤝🌐🪄
