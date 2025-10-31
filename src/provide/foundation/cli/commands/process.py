#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.console.output import perr, pout
from provide.foundation.process.title import (
    get_process_title,
    has_setproctitle,
    set_process_title,
)

"""CLI commands for process title management."""


def _set_title_impl(title: str) -> None:
    """Implementation of set-title command logic."""
    if not has_setproctitle():
        perr("⚠️  Process title support not available")
        perr("Install with: pip install 'provide-foundation[process]'")
        return

    set_process_title(title)


def _get_title_impl() -> None:
    """Implementation of get-title command logic."""
    if not has_setproctitle():
        perr("⚠️  Process title support not available")
        perr("Install with: pip install 'provide-foundation[process]'")
        return

    title = get_process_title()
    pout(f"Current process title: {title}")


def _info_impl() -> None:
    """Implementation of info command logic."""
    if has_setproctitle():
        current = get_process_title()
        pout(f"Current title: {current}")
    else:
        pout("⚠️  Process title support: Not available")
        pout("Install with: pip install 'provide-foundation[process]'")


@click.group("process")
def process_group() -> None:
    """Process management commands.

    Commands for managing process titles and process information.
    Requires the 'process' extra: pip install 'provide-foundation[process]'
    """
    pass


@process_group.command("set-title")
@click.argument("title")
@requires_click
@with_cleanup
def set_title_command(title: str) -> None:
    """Set the current process title.

    The process title appears in process listings (ps, top, etc.) and helps
    identify processes in monitoring tools.

    Example:
        foundation process set-title "my-worker-1"
    """
    _set_title_impl(title)


@process_group.command("get-title")
@requires_click
@with_cleanup
def get_title_command() -> None:
    """Get the current process title.

    Displays the current process title as it appears in process listings.

    Example:
        foundation process get-title
    """
    _get_title_impl()


@process_group.command("info")
@requires_click
@with_cleanup
def info_command() -> None:
    """Show process title support information.

    Displays whether process title support is available and the current
    process title if supported.

    Example:
        foundation process info
    """
    _info_impl()


# Export the command group
__all__ = ["process_group"]

# 🧱🏗️🔚
