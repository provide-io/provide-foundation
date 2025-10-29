# provide/foundation/cli/main.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Main CLI entry point for Foundation."""

from __future__ import annotations

from provide.foundation.cli.deps import _HAS_CLICK, click
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


def x__require_click__mutmut_orig() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            "CLI requires optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )


def x__require_click__mutmut_1() -> None:
    """Ensure click is available for CLI."""
    if _HAS_CLICK:
        raise ImportError(
            "CLI requires optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )


def x__require_click__mutmut_2() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            None,
        )


def x__require_click__mutmut_3() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            "XXCLI requires optional dependencies. Install with: pip install 'provide-foundation[cli]'XX",
        )


def x__require_click__mutmut_4() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            "cli requires optional dependencies. install with: pip install 'provide-foundation[cli]'",
        )


def x__require_click__mutmut_5() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            "CLI REQUIRES OPTIONAL DEPENDENCIES. INSTALL WITH: PIP INSTALL 'PROVIDE-FOUNDATION[CLI]'",
        )


x__require_click__mutmut_mutants: ClassVar[MutantDict] = {
    "x__require_click__mutmut_1": x__require_click__mutmut_1,
    "x__require_click__mutmut_2": x__require_click__mutmut_2,
    "x__require_click__mutmut_3": x__require_click__mutmut_3,
    "x__require_click__mutmut_4": x__require_click__mutmut_4,
    "x__require_click__mutmut_5": x__require_click__mutmut_5,
}


def _require_click(*args, **kwargs):
    result = _mutmut_trampoline(x__require_click__mutmut_orig, x__require_click__mutmut_mutants, args, kwargs)
    return result


_require_click.__signature__ = _mutmut_signature(x__require_click__mutmut_orig)
x__require_click__mutmut_orig.__name__ = "x__require_click"


if _HAS_CLICK:

    @click.group()
    @click.version_option()
    def cli() -> None:
        """Foundation CLI - Telemetry and observability tools."""
        # Register cleanup handlers on CLI startup
        from provide.foundation.cli.shutdown import register_cleanup_handlers

        register_cleanup_handlers()

    # Register commands from commands module
    try:
        from provide.foundation.cli.commands.deps import deps_command

        if hasattr(deps_command, "callback"):
            cli.add_command(deps_command)
    except ImportError:
        pass

    # Register config commands
    try:
        from provide.foundation.cli.commands.config import config_group

        if hasattr(config_group, "callback"):
            cli.add_command(config_group)
    except ImportError:
        pass

    # Register logs commands
    try:
        from provide.foundation.cli.commands.logs import logs_group

        if hasattr(logs_group, "callback"):
            cli.add_command(logs_group)
    except ImportError:
        pass

    # Register OpenObserve commands if available
    try:
        from provide.foundation.integrations.openobserve.commands import (
            openobserve_group,
        )

        if hasattr(openobserve_group, "callback"):
            cli.add_command(openobserve_group)
    except ImportError:
        pass

else:

    def cli() -> None:
        """CLI stub when click is not available."""
        _require_click()


if __name__ == "__main__":
    cli()


# <3 🧱🤝💻🪄
