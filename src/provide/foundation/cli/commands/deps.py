#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.console.output import pout
from provide.foundation.process import exit_error, exit_success
from provide.foundation.utils.deps import check_optional_deps, has_dependency

"""CLI command for checking optional dependencies."""


def _deps_command_impl(quiet: bool, check: str | None) -> None:
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

# 🧱🏗️🔚
