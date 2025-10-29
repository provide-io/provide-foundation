# provide/foundation/utils/deps.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from attrs import define

"""Optional dependency checking utilities."""
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
class DependencyStatus:
    """Status of an optional dependency."""

    name: str
    available: bool
    version: str | None
    description: str


def x__check_click__mutmut_orig() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_1() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = None
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_2() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version(None)
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_3() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("XXclickXX")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_4() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("CLICK")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_5() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = None
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_6() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "XXunknownXX"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_7() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "UNKNOWN"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_8() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name=None,
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_9() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=None,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_10() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=None,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_11() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description=None,
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_12() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_13() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_14() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_15() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_16() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="XXclickXX",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_17() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="CLICK",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_18() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=False,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_19() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="XXCLI features (console I/O, command building)XX",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_20() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="cli features (console i/o, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_21() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI FEATURES (CONSOLE I/O, COMMAND BUILDING)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_22() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name=None,
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_23() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=None,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_24() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description=None,
        )


def x__check_click__mutmut_25() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_26() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_27() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_28() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
        )


def x__check_click__mutmut_29() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="XXclickXX",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_30() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="CLICK",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_31() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=True,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def x__check_click__mutmut_32() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="XXCLI features (console I/O, command building)XX",
        )


def x__check_click__mutmut_33() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="cli features (console i/o, command building)",
        )


def x__check_click__mutmut_34() -> DependencyStatus:
    """Check click availability."""
    try:
        import click  # noqa: F401

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("click")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI FEATURES (CONSOLE I/O, COMMAND BUILDING)",
        )


x__check_click__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_click__mutmut_1": x__check_click__mutmut_1,
    "x__check_click__mutmut_2": x__check_click__mutmut_2,
    "x__check_click__mutmut_3": x__check_click__mutmut_3,
    "x__check_click__mutmut_4": x__check_click__mutmut_4,
    "x__check_click__mutmut_5": x__check_click__mutmut_5,
    "x__check_click__mutmut_6": x__check_click__mutmut_6,
    "x__check_click__mutmut_7": x__check_click__mutmut_7,
    "x__check_click__mutmut_8": x__check_click__mutmut_8,
    "x__check_click__mutmut_9": x__check_click__mutmut_9,
    "x__check_click__mutmut_10": x__check_click__mutmut_10,
    "x__check_click__mutmut_11": x__check_click__mutmut_11,
    "x__check_click__mutmut_12": x__check_click__mutmut_12,
    "x__check_click__mutmut_13": x__check_click__mutmut_13,
    "x__check_click__mutmut_14": x__check_click__mutmut_14,
    "x__check_click__mutmut_15": x__check_click__mutmut_15,
    "x__check_click__mutmut_16": x__check_click__mutmut_16,
    "x__check_click__mutmut_17": x__check_click__mutmut_17,
    "x__check_click__mutmut_18": x__check_click__mutmut_18,
    "x__check_click__mutmut_19": x__check_click__mutmut_19,
    "x__check_click__mutmut_20": x__check_click__mutmut_20,
    "x__check_click__mutmut_21": x__check_click__mutmut_21,
    "x__check_click__mutmut_22": x__check_click__mutmut_22,
    "x__check_click__mutmut_23": x__check_click__mutmut_23,
    "x__check_click__mutmut_24": x__check_click__mutmut_24,
    "x__check_click__mutmut_25": x__check_click__mutmut_25,
    "x__check_click__mutmut_26": x__check_click__mutmut_26,
    "x__check_click__mutmut_27": x__check_click__mutmut_27,
    "x__check_click__mutmut_28": x__check_click__mutmut_28,
    "x__check_click__mutmut_29": x__check_click__mutmut_29,
    "x__check_click__mutmut_30": x__check_click__mutmut_30,
    "x__check_click__mutmut_31": x__check_click__mutmut_31,
    "x__check_click__mutmut_32": x__check_click__mutmut_32,
    "x__check_click__mutmut_33": x__check_click__mutmut_33,
    "x__check_click__mutmut_34": x__check_click__mutmut_34,
}


def _check_click(*args, **kwargs):
    result = _mutmut_trampoline(x__check_click__mutmut_orig, x__check_click__mutmut_mutants, args, kwargs)
    return result


_check_click.__signature__ = _mutmut_signature(x__check_click__mutmut_orig)
x__check_click__mutmut_orig.__name__ = "x__check_click"


def x__check_cryptography__mutmut_orig() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_1() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = None

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_2() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(None, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_3() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, None, "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_4() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", None)

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_5() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr("__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_6() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_7() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(
            cryptography,
            "__version__",
        )

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_8() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "XX__version__XX", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_9() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__VERSION__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_10() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "XXunknownXX")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_11() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "UNKNOWN")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_12() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name=None,
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_13() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=None,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_14() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_15() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description=None,
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_16() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_17() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_18() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_19() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_20() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="XXcryptographyXX",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_21() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="CRYPTOGRAPHY",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_22() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=False,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_23() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="XXCrypto features (keys, certificates, signatures)XX",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_24() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_25() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="CRYPTO FEATURES (KEYS, CERTIFICATES, SIGNATURES)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_26() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name=None,
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_27() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=None,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_28() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description=None,
        )


def x__check_cryptography__mutmut_29() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_30() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_31() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_32() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
        )


def x__check_cryptography__mutmut_33() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="XXcryptographyXX",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_34() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="CRYPTOGRAPHY",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_35() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=True,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_36() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="XXCrypto features (keys, certificates, signatures)XX",
        )


def x__check_cryptography__mutmut_37() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="crypto features (keys, certificates, signatures)",
        )


def x__check_cryptography__mutmut_38() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        # Get version safely
        version = getattr(cryptography, "__version__", "unknown")

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=version,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="CRYPTO FEATURES (KEYS, CERTIFICATES, SIGNATURES)",
        )


x__check_cryptography__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_cryptography__mutmut_1": x__check_cryptography__mutmut_1,
    "x__check_cryptography__mutmut_2": x__check_cryptography__mutmut_2,
    "x__check_cryptography__mutmut_3": x__check_cryptography__mutmut_3,
    "x__check_cryptography__mutmut_4": x__check_cryptography__mutmut_4,
    "x__check_cryptography__mutmut_5": x__check_cryptography__mutmut_5,
    "x__check_cryptography__mutmut_6": x__check_cryptography__mutmut_6,
    "x__check_cryptography__mutmut_7": x__check_cryptography__mutmut_7,
    "x__check_cryptography__mutmut_8": x__check_cryptography__mutmut_8,
    "x__check_cryptography__mutmut_9": x__check_cryptography__mutmut_9,
    "x__check_cryptography__mutmut_10": x__check_cryptography__mutmut_10,
    "x__check_cryptography__mutmut_11": x__check_cryptography__mutmut_11,
    "x__check_cryptography__mutmut_12": x__check_cryptography__mutmut_12,
    "x__check_cryptography__mutmut_13": x__check_cryptography__mutmut_13,
    "x__check_cryptography__mutmut_14": x__check_cryptography__mutmut_14,
    "x__check_cryptography__mutmut_15": x__check_cryptography__mutmut_15,
    "x__check_cryptography__mutmut_16": x__check_cryptography__mutmut_16,
    "x__check_cryptography__mutmut_17": x__check_cryptography__mutmut_17,
    "x__check_cryptography__mutmut_18": x__check_cryptography__mutmut_18,
    "x__check_cryptography__mutmut_19": x__check_cryptography__mutmut_19,
    "x__check_cryptography__mutmut_20": x__check_cryptography__mutmut_20,
    "x__check_cryptography__mutmut_21": x__check_cryptography__mutmut_21,
    "x__check_cryptography__mutmut_22": x__check_cryptography__mutmut_22,
    "x__check_cryptography__mutmut_23": x__check_cryptography__mutmut_23,
    "x__check_cryptography__mutmut_24": x__check_cryptography__mutmut_24,
    "x__check_cryptography__mutmut_25": x__check_cryptography__mutmut_25,
    "x__check_cryptography__mutmut_26": x__check_cryptography__mutmut_26,
    "x__check_cryptography__mutmut_27": x__check_cryptography__mutmut_27,
    "x__check_cryptography__mutmut_28": x__check_cryptography__mutmut_28,
    "x__check_cryptography__mutmut_29": x__check_cryptography__mutmut_29,
    "x__check_cryptography__mutmut_30": x__check_cryptography__mutmut_30,
    "x__check_cryptography__mutmut_31": x__check_cryptography__mutmut_31,
    "x__check_cryptography__mutmut_32": x__check_cryptography__mutmut_32,
    "x__check_cryptography__mutmut_33": x__check_cryptography__mutmut_33,
    "x__check_cryptography__mutmut_34": x__check_cryptography__mutmut_34,
    "x__check_cryptography__mutmut_35": x__check_cryptography__mutmut_35,
    "x__check_cryptography__mutmut_36": x__check_cryptography__mutmut_36,
    "x__check_cryptography__mutmut_37": x__check_cryptography__mutmut_37,
    "x__check_cryptography__mutmut_38": x__check_cryptography__mutmut_38,
}


def _check_cryptography(*args, **kwargs):
    result = _mutmut_trampoline(
        x__check_cryptography__mutmut_orig, x__check_cryptography__mutmut_mutants, args, kwargs
    )
    return result


_check_cryptography.__signature__ = _mutmut_signature(x__check_cryptography__mutmut_orig)
x__check_cryptography__mutmut_orig.__name__ = "x__check_cryptography"


def x__check_opentelemetry__mutmut_orig() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_1() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = None
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_2() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version(None)
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_3() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("XXopentelemetry-apiXX")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_4() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("OPENTELEMETRY-API")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_5() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = None
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_6() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "XXunknownXX"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_7() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "UNKNOWN"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_8() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name=None,
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_9() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=None,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_10() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=None,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_11() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description=None,
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_12() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_13() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_14() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_15() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_16() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="XXopentelemetryXX",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_17() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="OPENTELEMETRY",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_18() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_19() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="XXEnhanced telemetry and tracingXX",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_20() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_21() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="ENHANCED TELEMETRY AND TRACING",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_22() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name=None,
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_23() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=None,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_24() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description=None,
        )


def x__check_opentelemetry__mutmut_25() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_26() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_27() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_28() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
        )


def x__check_opentelemetry__mutmut_29() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="XXopentelemetryXX",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_30() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="OPENTELEMETRY",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_31() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_32() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="XXEnhanced telemetry and tracingXX",
        )


def x__check_opentelemetry__mutmut_33() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="enhanced telemetry and tracing",
        )


def x__check_opentelemetry__mutmut_34() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("opentelemetry-api")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="ENHANCED TELEMETRY AND TRACING",
        )


x__check_opentelemetry__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_opentelemetry__mutmut_1": x__check_opentelemetry__mutmut_1,
    "x__check_opentelemetry__mutmut_2": x__check_opentelemetry__mutmut_2,
    "x__check_opentelemetry__mutmut_3": x__check_opentelemetry__mutmut_3,
    "x__check_opentelemetry__mutmut_4": x__check_opentelemetry__mutmut_4,
    "x__check_opentelemetry__mutmut_5": x__check_opentelemetry__mutmut_5,
    "x__check_opentelemetry__mutmut_6": x__check_opentelemetry__mutmut_6,
    "x__check_opentelemetry__mutmut_7": x__check_opentelemetry__mutmut_7,
    "x__check_opentelemetry__mutmut_8": x__check_opentelemetry__mutmut_8,
    "x__check_opentelemetry__mutmut_9": x__check_opentelemetry__mutmut_9,
    "x__check_opentelemetry__mutmut_10": x__check_opentelemetry__mutmut_10,
    "x__check_opentelemetry__mutmut_11": x__check_opentelemetry__mutmut_11,
    "x__check_opentelemetry__mutmut_12": x__check_opentelemetry__mutmut_12,
    "x__check_opentelemetry__mutmut_13": x__check_opentelemetry__mutmut_13,
    "x__check_opentelemetry__mutmut_14": x__check_opentelemetry__mutmut_14,
    "x__check_opentelemetry__mutmut_15": x__check_opentelemetry__mutmut_15,
    "x__check_opentelemetry__mutmut_16": x__check_opentelemetry__mutmut_16,
    "x__check_opentelemetry__mutmut_17": x__check_opentelemetry__mutmut_17,
    "x__check_opentelemetry__mutmut_18": x__check_opentelemetry__mutmut_18,
    "x__check_opentelemetry__mutmut_19": x__check_opentelemetry__mutmut_19,
    "x__check_opentelemetry__mutmut_20": x__check_opentelemetry__mutmut_20,
    "x__check_opentelemetry__mutmut_21": x__check_opentelemetry__mutmut_21,
    "x__check_opentelemetry__mutmut_22": x__check_opentelemetry__mutmut_22,
    "x__check_opentelemetry__mutmut_23": x__check_opentelemetry__mutmut_23,
    "x__check_opentelemetry__mutmut_24": x__check_opentelemetry__mutmut_24,
    "x__check_opentelemetry__mutmut_25": x__check_opentelemetry__mutmut_25,
    "x__check_opentelemetry__mutmut_26": x__check_opentelemetry__mutmut_26,
    "x__check_opentelemetry__mutmut_27": x__check_opentelemetry__mutmut_27,
    "x__check_opentelemetry__mutmut_28": x__check_opentelemetry__mutmut_28,
    "x__check_opentelemetry__mutmut_29": x__check_opentelemetry__mutmut_29,
    "x__check_opentelemetry__mutmut_30": x__check_opentelemetry__mutmut_30,
    "x__check_opentelemetry__mutmut_31": x__check_opentelemetry__mutmut_31,
    "x__check_opentelemetry__mutmut_32": x__check_opentelemetry__mutmut_32,
    "x__check_opentelemetry__mutmut_33": x__check_opentelemetry__mutmut_33,
    "x__check_opentelemetry__mutmut_34": x__check_opentelemetry__mutmut_34,
}


def _check_opentelemetry(*args, **kwargs):
    result = _mutmut_trampoline(
        x__check_opentelemetry__mutmut_orig, x__check_opentelemetry__mutmut_mutants, args, kwargs
    )
    return result


_check_opentelemetry.__signature__ = _mutmut_signature(x__check_opentelemetry__mutmut_orig)
x__check_opentelemetry__mutmut_orig.__name__ = "x__check_opentelemetry"


def x__check_httpx__mutmut_orig() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_1() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = None

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_2() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(None, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_3() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, None, "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_4() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", None)

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_5() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr("__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_6() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_7() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(
            httpx,
            "__version__",
        )

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_8() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "XX__version__XX", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_9() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__VERSION__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_10() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "XXunknownXX")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_11() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "UNKNOWN")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_12() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name=None,
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_13() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=None,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_14() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=None,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_15() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description=None,
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_16() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_17() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_18() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_19() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_20() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="XXhttpxXX",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_21() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="HTTPX",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_22() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=False,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_23() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="XXHTTP/HTTPS transport supportXX",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_24() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="http/https transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_25() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS TRANSPORT SUPPORT",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_26() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name=None,
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_27() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=None,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_28() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description=None,
        )


def x__check_httpx__mutmut_29() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_30() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_31() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_32() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
        )


def x__check_httpx__mutmut_33() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="XXhttpxXX",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_34() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="HTTPX",
            available=False,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_35() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=True,
            version=None,
            description="HTTP/HTTPS transport support",
        )


def x__check_httpx__mutmut_36() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="XXHTTP/HTTPS transport supportXX",
        )


def x__check_httpx__mutmut_37() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="http/https transport support",
        )


def x__check_httpx__mutmut_38() -> DependencyStatus:
    """Check httpx availability for transport support."""
    try:
        import httpx

        # Get version safely
        version = getattr(httpx, "__version__", "unknown")

        return DependencyStatus(
            name="httpx",
            available=True,
            version=version,
            description="HTTP/HTTPS transport support",
        )
    except ImportError:
        return DependencyStatus(
            name="httpx",
            available=False,
            version=None,
            description="HTTP/HTTPS TRANSPORT SUPPORT",
        )


x__check_httpx__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_httpx__mutmut_1": x__check_httpx__mutmut_1,
    "x__check_httpx__mutmut_2": x__check_httpx__mutmut_2,
    "x__check_httpx__mutmut_3": x__check_httpx__mutmut_3,
    "x__check_httpx__mutmut_4": x__check_httpx__mutmut_4,
    "x__check_httpx__mutmut_5": x__check_httpx__mutmut_5,
    "x__check_httpx__mutmut_6": x__check_httpx__mutmut_6,
    "x__check_httpx__mutmut_7": x__check_httpx__mutmut_7,
    "x__check_httpx__mutmut_8": x__check_httpx__mutmut_8,
    "x__check_httpx__mutmut_9": x__check_httpx__mutmut_9,
    "x__check_httpx__mutmut_10": x__check_httpx__mutmut_10,
    "x__check_httpx__mutmut_11": x__check_httpx__mutmut_11,
    "x__check_httpx__mutmut_12": x__check_httpx__mutmut_12,
    "x__check_httpx__mutmut_13": x__check_httpx__mutmut_13,
    "x__check_httpx__mutmut_14": x__check_httpx__mutmut_14,
    "x__check_httpx__mutmut_15": x__check_httpx__mutmut_15,
    "x__check_httpx__mutmut_16": x__check_httpx__mutmut_16,
    "x__check_httpx__mutmut_17": x__check_httpx__mutmut_17,
    "x__check_httpx__mutmut_18": x__check_httpx__mutmut_18,
    "x__check_httpx__mutmut_19": x__check_httpx__mutmut_19,
    "x__check_httpx__mutmut_20": x__check_httpx__mutmut_20,
    "x__check_httpx__mutmut_21": x__check_httpx__mutmut_21,
    "x__check_httpx__mutmut_22": x__check_httpx__mutmut_22,
    "x__check_httpx__mutmut_23": x__check_httpx__mutmut_23,
    "x__check_httpx__mutmut_24": x__check_httpx__mutmut_24,
    "x__check_httpx__mutmut_25": x__check_httpx__mutmut_25,
    "x__check_httpx__mutmut_26": x__check_httpx__mutmut_26,
    "x__check_httpx__mutmut_27": x__check_httpx__mutmut_27,
    "x__check_httpx__mutmut_28": x__check_httpx__mutmut_28,
    "x__check_httpx__mutmut_29": x__check_httpx__mutmut_29,
    "x__check_httpx__mutmut_30": x__check_httpx__mutmut_30,
    "x__check_httpx__mutmut_31": x__check_httpx__mutmut_31,
    "x__check_httpx__mutmut_32": x__check_httpx__mutmut_32,
    "x__check_httpx__mutmut_33": x__check_httpx__mutmut_33,
    "x__check_httpx__mutmut_34": x__check_httpx__mutmut_34,
    "x__check_httpx__mutmut_35": x__check_httpx__mutmut_35,
    "x__check_httpx__mutmut_36": x__check_httpx__mutmut_36,
    "x__check_httpx__mutmut_37": x__check_httpx__mutmut_37,
    "x__check_httpx__mutmut_38": x__check_httpx__mutmut_38,
}


def _check_httpx(*args, **kwargs):
    result = _mutmut_trampoline(x__check_httpx__mutmut_orig, x__check_httpx__mutmut_mutants, args, kwargs)
    return result


_check_httpx.__signature__ = _mutmut_signature(x__check_httpx__mutmut_orig)
x__check_httpx__mutmut_orig.__name__ = "x__check_httpx"


def x__check_mkdocs__mutmut_orig() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_1() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = None
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_2() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version(None)
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_3() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("XXmkdocsXX")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_4() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("MKDOCS")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_5() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = None
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_6() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "XXunknownXX"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_7() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "UNKNOWN"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_8() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name=None,
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_9() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=None,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_10() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=None,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_11() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description=None,
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_12() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_13() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_14() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_15() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_16() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="XXmkdocsXX",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_17() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="MKDOCS",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_18() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_19() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="XXDocumentation generation supportXX",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_20() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_21() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="DOCUMENTATION GENERATION SUPPORT",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_22() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name=None,
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_23() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=None,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_24() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description=None,
        )


def x__check_mkdocs__mutmut_25() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_26() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_27() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_28() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
        )


def x__check_mkdocs__mutmut_29() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="XXmkdocsXX",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_30() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="MKDOCS",
            available=False,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_31() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=None,
            description="Documentation generation support",
        )


def x__check_mkdocs__mutmut_32() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="XXDocumentation generation supportXX",
        )


def x__check_mkdocs__mutmut_33() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="documentation generation support",
        )


def x__check_mkdocs__mutmut_34() -> DependencyStatus:
    """Check mkdocs availability for documentation generation."""
    try:
        import mkdocs  # noqa: F401

        try:
            from importlib.metadata import PackageNotFoundError, version

            ver = version("mkdocs")
        except (PackageNotFoundError, Exception):
            # PackageNotFoundError: Package metadata not found
            # Exception: Fallback for other version() failures (including mocked tests)
            ver = "unknown"
        return DependencyStatus(
            name="mkdocs",
            available=True,
            version=ver,
            description="Documentation generation support",
        )
    except ImportError:
        return DependencyStatus(
            name="mkdocs",
            available=False,
            version=None,
            description="DOCUMENTATION GENERATION SUPPORT",
        )


x__check_mkdocs__mutmut_mutants: ClassVar[MutantDict] = {
    "x__check_mkdocs__mutmut_1": x__check_mkdocs__mutmut_1,
    "x__check_mkdocs__mutmut_2": x__check_mkdocs__mutmut_2,
    "x__check_mkdocs__mutmut_3": x__check_mkdocs__mutmut_3,
    "x__check_mkdocs__mutmut_4": x__check_mkdocs__mutmut_4,
    "x__check_mkdocs__mutmut_5": x__check_mkdocs__mutmut_5,
    "x__check_mkdocs__mutmut_6": x__check_mkdocs__mutmut_6,
    "x__check_mkdocs__mutmut_7": x__check_mkdocs__mutmut_7,
    "x__check_mkdocs__mutmut_8": x__check_mkdocs__mutmut_8,
    "x__check_mkdocs__mutmut_9": x__check_mkdocs__mutmut_9,
    "x__check_mkdocs__mutmut_10": x__check_mkdocs__mutmut_10,
    "x__check_mkdocs__mutmut_11": x__check_mkdocs__mutmut_11,
    "x__check_mkdocs__mutmut_12": x__check_mkdocs__mutmut_12,
    "x__check_mkdocs__mutmut_13": x__check_mkdocs__mutmut_13,
    "x__check_mkdocs__mutmut_14": x__check_mkdocs__mutmut_14,
    "x__check_mkdocs__mutmut_15": x__check_mkdocs__mutmut_15,
    "x__check_mkdocs__mutmut_16": x__check_mkdocs__mutmut_16,
    "x__check_mkdocs__mutmut_17": x__check_mkdocs__mutmut_17,
    "x__check_mkdocs__mutmut_18": x__check_mkdocs__mutmut_18,
    "x__check_mkdocs__mutmut_19": x__check_mkdocs__mutmut_19,
    "x__check_mkdocs__mutmut_20": x__check_mkdocs__mutmut_20,
    "x__check_mkdocs__mutmut_21": x__check_mkdocs__mutmut_21,
    "x__check_mkdocs__mutmut_22": x__check_mkdocs__mutmut_22,
    "x__check_mkdocs__mutmut_23": x__check_mkdocs__mutmut_23,
    "x__check_mkdocs__mutmut_24": x__check_mkdocs__mutmut_24,
    "x__check_mkdocs__mutmut_25": x__check_mkdocs__mutmut_25,
    "x__check_mkdocs__mutmut_26": x__check_mkdocs__mutmut_26,
    "x__check_mkdocs__mutmut_27": x__check_mkdocs__mutmut_27,
    "x__check_mkdocs__mutmut_28": x__check_mkdocs__mutmut_28,
    "x__check_mkdocs__mutmut_29": x__check_mkdocs__mutmut_29,
    "x__check_mkdocs__mutmut_30": x__check_mkdocs__mutmut_30,
    "x__check_mkdocs__mutmut_31": x__check_mkdocs__mutmut_31,
    "x__check_mkdocs__mutmut_32": x__check_mkdocs__mutmut_32,
    "x__check_mkdocs__mutmut_33": x__check_mkdocs__mutmut_33,
    "x__check_mkdocs__mutmut_34": x__check_mkdocs__mutmut_34,
}


def _check_mkdocs(*args, **kwargs):
    result = _mutmut_trampoline(x__check_mkdocs__mutmut_orig, x__check_mkdocs__mutmut_mutants, args, kwargs)
    return result


_check_mkdocs.__signature__ = _mutmut_signature(x__check_mkdocs__mutmut_orig)
x__check_mkdocs__mutmut_orig.__name__ = "x__check_mkdocs"


def get_optional_dependencies() -> list[DependencyStatus]:
    """Get status of all optional dependencies.

    Returns:
        List of dependency status objects

    """
    return [
        _check_click(),
        _check_cryptography(),
        _check_httpx(),
        _check_mkdocs(),
        _check_opentelemetry(),
    ]


def x_check_optional_deps__mutmut_orig(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_1(
    *, quiet: bool = True, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_2(
    *, quiet: bool = False, return_status: bool = True
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_3(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = None

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_4(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_5(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = None
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_6(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info(None)
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_7(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("XX📦 provide-foundation Optional Dependencies StatusXX")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_8(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation optional dependencies status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_9(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 PROVIDE-FOUNDATION OPTIONAL DEPENDENCIES STATUS")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_10(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info(None)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_11(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" / 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_12(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("XX=XX" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_13(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 51)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_14(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = None
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_15(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(None)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_16(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(2 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_17(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = None

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_18(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = None
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_19(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "XX✅XX" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_20(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "XX❌XX"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_21(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = None
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_22(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else "XXXX"
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_23(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(None)
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_24(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(None)
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_25(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_26(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(None)

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_27(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(None)

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_28(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count != total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_29(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info(None)
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_30(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("XX🎉 All optional features are available!XX")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_31(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 all optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_32(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 ALL OPTIONAL FEATURES ARE AVAILABLE!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_33(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count != 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_34(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 1:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_35(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info(None)
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_36(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("XX💡 Install optional features with: pip install 'provide-foundation[all]'XX")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_37(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_38(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 INSTALL OPTIONAL FEATURES WITH: PIP INSTALL 'PROVIDE-FOUNDATION[ALL]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_39(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = None
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_40(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_41(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(None)

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_42(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(None)}")

    if return_status:
        return deps
    return None


def x_check_optional_deps__mutmut_43(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True

    """
    deps = get_optional_dependencies()

    if not quiet:
        from provide.foundation.hub.foundation import get_foundation_logger

        log = get_foundation_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(f"     Install with: pip install 'provide-foundation[{dep.name}]'")

        log.info(f"📊 Summary: {available_count}/{total_count} optional dependencies available")

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info("💡 Install optional features with: pip install 'provide-foundation[all]'")
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {'XX, XX'.join(missing)}")

    if return_status:
        return deps
    return None


x_check_optional_deps__mutmut_mutants: ClassVar[MutantDict] = {
    "x_check_optional_deps__mutmut_1": x_check_optional_deps__mutmut_1,
    "x_check_optional_deps__mutmut_2": x_check_optional_deps__mutmut_2,
    "x_check_optional_deps__mutmut_3": x_check_optional_deps__mutmut_3,
    "x_check_optional_deps__mutmut_4": x_check_optional_deps__mutmut_4,
    "x_check_optional_deps__mutmut_5": x_check_optional_deps__mutmut_5,
    "x_check_optional_deps__mutmut_6": x_check_optional_deps__mutmut_6,
    "x_check_optional_deps__mutmut_7": x_check_optional_deps__mutmut_7,
    "x_check_optional_deps__mutmut_8": x_check_optional_deps__mutmut_8,
    "x_check_optional_deps__mutmut_9": x_check_optional_deps__mutmut_9,
    "x_check_optional_deps__mutmut_10": x_check_optional_deps__mutmut_10,
    "x_check_optional_deps__mutmut_11": x_check_optional_deps__mutmut_11,
    "x_check_optional_deps__mutmut_12": x_check_optional_deps__mutmut_12,
    "x_check_optional_deps__mutmut_13": x_check_optional_deps__mutmut_13,
    "x_check_optional_deps__mutmut_14": x_check_optional_deps__mutmut_14,
    "x_check_optional_deps__mutmut_15": x_check_optional_deps__mutmut_15,
    "x_check_optional_deps__mutmut_16": x_check_optional_deps__mutmut_16,
    "x_check_optional_deps__mutmut_17": x_check_optional_deps__mutmut_17,
    "x_check_optional_deps__mutmut_18": x_check_optional_deps__mutmut_18,
    "x_check_optional_deps__mutmut_19": x_check_optional_deps__mutmut_19,
    "x_check_optional_deps__mutmut_20": x_check_optional_deps__mutmut_20,
    "x_check_optional_deps__mutmut_21": x_check_optional_deps__mutmut_21,
    "x_check_optional_deps__mutmut_22": x_check_optional_deps__mutmut_22,
    "x_check_optional_deps__mutmut_23": x_check_optional_deps__mutmut_23,
    "x_check_optional_deps__mutmut_24": x_check_optional_deps__mutmut_24,
    "x_check_optional_deps__mutmut_25": x_check_optional_deps__mutmut_25,
    "x_check_optional_deps__mutmut_26": x_check_optional_deps__mutmut_26,
    "x_check_optional_deps__mutmut_27": x_check_optional_deps__mutmut_27,
    "x_check_optional_deps__mutmut_28": x_check_optional_deps__mutmut_28,
    "x_check_optional_deps__mutmut_29": x_check_optional_deps__mutmut_29,
    "x_check_optional_deps__mutmut_30": x_check_optional_deps__mutmut_30,
    "x_check_optional_deps__mutmut_31": x_check_optional_deps__mutmut_31,
    "x_check_optional_deps__mutmut_32": x_check_optional_deps__mutmut_32,
    "x_check_optional_deps__mutmut_33": x_check_optional_deps__mutmut_33,
    "x_check_optional_deps__mutmut_34": x_check_optional_deps__mutmut_34,
    "x_check_optional_deps__mutmut_35": x_check_optional_deps__mutmut_35,
    "x_check_optional_deps__mutmut_36": x_check_optional_deps__mutmut_36,
    "x_check_optional_deps__mutmut_37": x_check_optional_deps__mutmut_37,
    "x_check_optional_deps__mutmut_38": x_check_optional_deps__mutmut_38,
    "x_check_optional_deps__mutmut_39": x_check_optional_deps__mutmut_39,
    "x_check_optional_deps__mutmut_40": x_check_optional_deps__mutmut_40,
    "x_check_optional_deps__mutmut_41": x_check_optional_deps__mutmut_41,
    "x_check_optional_deps__mutmut_42": x_check_optional_deps__mutmut_42,
    "x_check_optional_deps__mutmut_43": x_check_optional_deps__mutmut_43,
}


def check_optional_deps(*args, **kwargs):
    result = _mutmut_trampoline(
        x_check_optional_deps__mutmut_orig, x_check_optional_deps__mutmut_mutants, args, kwargs
    )
    return result


check_optional_deps.__signature__ = _mutmut_signature(x_check_optional_deps__mutmut_orig)
x_check_optional_deps__mutmut_orig.__name__ = "x_check_optional_deps"


def x_has_dependency__mutmut_orig(name: str) -> bool:
    """Check if a specific optional dependency is available.

    Args:
        name: Name of the dependency to check

    Returns:
        True if dependency is available

    """
    deps = get_optional_dependencies()
    for dep in deps:
        if dep.name == name:
            return dep.available
    return False


def x_has_dependency__mutmut_1(name: str) -> bool:
    """Check if a specific optional dependency is available.

    Args:
        name: Name of the dependency to check

    Returns:
        True if dependency is available

    """
    deps = None
    for dep in deps:
        if dep.name == name:
            return dep.available
    return False


def x_has_dependency__mutmut_2(name: str) -> bool:
    """Check if a specific optional dependency is available.

    Args:
        name: Name of the dependency to check

    Returns:
        True if dependency is available

    """
    deps = get_optional_dependencies()
    for dep in deps:
        if dep.name != name:
            return dep.available
    return False


def x_has_dependency__mutmut_3(name: str) -> bool:
    """Check if a specific optional dependency is available.

    Args:
        name: Name of the dependency to check

    Returns:
        True if dependency is available

    """
    deps = get_optional_dependencies()
    for dep in deps:
        if dep.name == name:
            return dep.available
    return True


x_has_dependency__mutmut_mutants: ClassVar[MutantDict] = {
    "x_has_dependency__mutmut_1": x_has_dependency__mutmut_1,
    "x_has_dependency__mutmut_2": x_has_dependency__mutmut_2,
    "x_has_dependency__mutmut_3": x_has_dependency__mutmut_3,
}


def has_dependency(*args, **kwargs):
    result = _mutmut_trampoline(x_has_dependency__mutmut_orig, x_has_dependency__mutmut_mutants, args, kwargs)
    return result


has_dependency.__signature__ = _mutmut_signature(x_has_dependency__mutmut_orig)
x_has_dependency__mutmut_orig.__name__ = "x_has_dependency"


def x_require_dependency__mutmut_orig(name: str) -> None:
    """Require a specific optional dependency, raise ImportError if missing.

    Args:
        name: Name of the dependency to require

    Raises:
        ImportError: If dependency is not available

    """
    if not has_dependency(name):
        raise ImportError(
            f"Optional dependency '{name}' is required for this feature. "
            f"Install with: pip install 'provide-foundation[{name}]'",
        )


def x_require_dependency__mutmut_1(name: str) -> None:
    """Require a specific optional dependency, raise ImportError if missing.

    Args:
        name: Name of the dependency to require

    Raises:
        ImportError: If dependency is not available

    """
    if has_dependency(name):
        raise ImportError(
            f"Optional dependency '{name}' is required for this feature. "
            f"Install with: pip install 'provide-foundation[{name}]'",
        )


def x_require_dependency__mutmut_2(name: str) -> None:
    """Require a specific optional dependency, raise ImportError if missing.

    Args:
        name: Name of the dependency to require

    Raises:
        ImportError: If dependency is not available

    """
    if not has_dependency(None):
        raise ImportError(
            f"Optional dependency '{name}' is required for this feature. "
            f"Install with: pip install 'provide-foundation[{name}]'",
        )


def x_require_dependency__mutmut_3(name: str) -> None:
    """Require a specific optional dependency, raise ImportError if missing.

    Args:
        name: Name of the dependency to require

    Raises:
        ImportError: If dependency is not available

    """
    if not has_dependency(name):
        raise ImportError(
            None,
        )


x_require_dependency__mutmut_mutants: ClassVar[MutantDict] = {
    "x_require_dependency__mutmut_1": x_require_dependency__mutmut_1,
    "x_require_dependency__mutmut_2": x_require_dependency__mutmut_2,
    "x_require_dependency__mutmut_3": x_require_dependency__mutmut_3,
}


def require_dependency(*args, **kwargs):
    result = _mutmut_trampoline(
        x_require_dependency__mutmut_orig, x_require_dependency__mutmut_mutants, args, kwargs
    )
    return result


require_dependency.__signature__ = _mutmut_signature(x_require_dependency__mutmut_orig)
x_require_dependency__mutmut_orig.__name__ = "x_require_dependency"


def x_get_available_features__mutmut_orig() -> dict[str, bool]:
    """Get a dictionary of available optional features.

    Returns:
        Dictionary mapping feature names to availability

    """
    deps = get_optional_dependencies()
    return {dep.name: dep.available for dep in deps}


def x_get_available_features__mutmut_1() -> dict[str, bool]:
    """Get a dictionary of available optional features.

    Returns:
        Dictionary mapping feature names to availability

    """
    deps = None
    return {dep.name: dep.available for dep in deps}


x_get_available_features__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_available_features__mutmut_1": x_get_available_features__mutmut_1
}


def get_available_features(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_available_features__mutmut_orig, x_get_available_features__mutmut_mutants, args, kwargs
    )
    return result


get_available_features.__signature__ = _mutmut_signature(x_get_available_features__mutmut_orig)
x_get_available_features__mutmut_orig.__name__ = "x_get_available_features"


# <3 🧱🤝🧰🪄
