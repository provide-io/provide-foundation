#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Main CLI entry point for Foundation."""

from __future__ import annotations

from provide.foundation.cli.deps import _HAS_CLICK, click


def _require_click() -> None:
    """Ensure click is available for CLI."""
    if not _HAS_CLICK:
        raise ImportError(
            "CLI requires optional dependencies. Install with: pip install 'provide-foundation[cli]'",
        )


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

    # Register process commands
    try:
        from provide.foundation.cli.commands.process import process_group

        if hasattr(process_group, "callback"):
            cli.add_command(process_group)
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

# 🧱🏗️🔚
