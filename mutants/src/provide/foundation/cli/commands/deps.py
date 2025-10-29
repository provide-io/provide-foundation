# provide/foundation/cli/commands/deps.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.console.output import pout
from provide.foundation.process import exit_error, exit_success
from provide.foundation.utils.deps import check_optional_deps, has_dependency

"""CLI command for checking optional dependencies."""
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


def x__deps_command_impl__mutmut_orig(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_1(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = None
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_2(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(None)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_3(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_4(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = None
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_5(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "XX✅XX" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_6(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "XX❌XX"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_7(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(None)
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_8(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'XXAvailableXX' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_9(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_10(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'AVAILABLE' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_11(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'XXMissingXX'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_12(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_13(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'MISSING'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_14(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_15(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(None)
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_16(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error(None)
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_17(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("XXDependency check failedXX")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_18(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_19(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("DEPENDENCY CHECK FAILED")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_20(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = None
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_21(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=None, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_22(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=None)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_23(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_24(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(
            quiet=quiet,
        )
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_25(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=False)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_26(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is not None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_27(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error(None)
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_28(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("XXFailed to check dependenciesXX")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_29(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_30(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("FAILED TO CHECK DEPENDENCIES")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_31(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = None
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_32(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(None)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_33(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(2 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_34(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = None
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_35(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count != total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count - available_count} dependencies")


def x__deps_command_impl__mutmut_36(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(None)


def x__deps_command_impl__mutmut_37(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            pout(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                pout(f"Install with: pip install 'provide-foundation[{check}]'")
        if available:
            exit_success()
        else:
            exit_error("Dependency check failed")
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        if deps is None:
            exit_error("Failed to check dependencies")
            return  # This line helps type checker understand deps is not None after this point

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        if available_count == total_count:
            exit_success()
        else:
            exit_error(f"Missing {total_count + available_count} dependencies")


x__deps_command_impl__mutmut_mutants: ClassVar[MutantDict] = {
    "x__deps_command_impl__mutmut_1": x__deps_command_impl__mutmut_1,
    "x__deps_command_impl__mutmut_2": x__deps_command_impl__mutmut_2,
    "x__deps_command_impl__mutmut_3": x__deps_command_impl__mutmut_3,
    "x__deps_command_impl__mutmut_4": x__deps_command_impl__mutmut_4,
    "x__deps_command_impl__mutmut_5": x__deps_command_impl__mutmut_5,
    "x__deps_command_impl__mutmut_6": x__deps_command_impl__mutmut_6,
    "x__deps_command_impl__mutmut_7": x__deps_command_impl__mutmut_7,
    "x__deps_command_impl__mutmut_8": x__deps_command_impl__mutmut_8,
    "x__deps_command_impl__mutmut_9": x__deps_command_impl__mutmut_9,
    "x__deps_command_impl__mutmut_10": x__deps_command_impl__mutmut_10,
    "x__deps_command_impl__mutmut_11": x__deps_command_impl__mutmut_11,
    "x__deps_command_impl__mutmut_12": x__deps_command_impl__mutmut_12,
    "x__deps_command_impl__mutmut_13": x__deps_command_impl__mutmut_13,
    "x__deps_command_impl__mutmut_14": x__deps_command_impl__mutmut_14,
    "x__deps_command_impl__mutmut_15": x__deps_command_impl__mutmut_15,
    "x__deps_command_impl__mutmut_16": x__deps_command_impl__mutmut_16,
    "x__deps_command_impl__mutmut_17": x__deps_command_impl__mutmut_17,
    "x__deps_command_impl__mutmut_18": x__deps_command_impl__mutmut_18,
    "x__deps_command_impl__mutmut_19": x__deps_command_impl__mutmut_19,
    "x__deps_command_impl__mutmut_20": x__deps_command_impl__mutmut_20,
    "x__deps_command_impl__mutmut_21": x__deps_command_impl__mutmut_21,
    "x__deps_command_impl__mutmut_22": x__deps_command_impl__mutmut_22,
    "x__deps_command_impl__mutmut_23": x__deps_command_impl__mutmut_23,
    "x__deps_command_impl__mutmut_24": x__deps_command_impl__mutmut_24,
    "x__deps_command_impl__mutmut_25": x__deps_command_impl__mutmut_25,
    "x__deps_command_impl__mutmut_26": x__deps_command_impl__mutmut_26,
    "x__deps_command_impl__mutmut_27": x__deps_command_impl__mutmut_27,
    "x__deps_command_impl__mutmut_28": x__deps_command_impl__mutmut_28,
    "x__deps_command_impl__mutmut_29": x__deps_command_impl__mutmut_29,
    "x__deps_command_impl__mutmut_30": x__deps_command_impl__mutmut_30,
    "x__deps_command_impl__mutmut_31": x__deps_command_impl__mutmut_31,
    "x__deps_command_impl__mutmut_32": x__deps_command_impl__mutmut_32,
    "x__deps_command_impl__mutmut_33": x__deps_command_impl__mutmut_33,
    "x__deps_command_impl__mutmut_34": x__deps_command_impl__mutmut_34,
    "x__deps_command_impl__mutmut_35": x__deps_command_impl__mutmut_35,
    "x__deps_command_impl__mutmut_36": x__deps_command_impl__mutmut_36,
    "x__deps_command_impl__mutmut_37": x__deps_command_impl__mutmut_37,
}


def _deps_command_impl(*args, **kwargs):
    result = _mutmut_trampoline(
        x__deps_command_impl__mutmut_orig, x__deps_command_impl__mutmut_mutants, args, kwargs
    )
    return result


_deps_command_impl.__signature__ = _mutmut_signature(x__deps_command_impl__mutmut_orig)
x__deps_command_impl__mutmut_orig.__name__ = "x__deps_command_impl"


@click.command("deps")
@click.option("--quiet", "-q", is_flag=True, help="Suppress output, just return exit code")
@click.option("--check", metavar="DEPENDENCY", help="Check specific dependency only")
@requires_click
@with_cleanup
def deps_command(quiet: bool, check: str | None) -> None:
    """Check optional dependency status.

    Shows which optional dependencies are available and provides
    installation instructions for missing ones.

    Exit codes:
    - 0: All dependencies available (or specific one if --check used)
    - 1: Some dependencies missing (or specific one missing if --check used)
    """
    _deps_command_impl(quiet, check)


# Export the command
__all__ = ["deps_command"]


# <3 🧱🤝💻🪄
