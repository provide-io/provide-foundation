"""Main CLI entry point for Foundation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import click

# Click feature detection
_click_module: Any = None
try:
    import click as _click_module

    _HAS_CLICK = True
except ImportError:
    _click_module = None
    _HAS_CLICK = False

# Use consistent name throughout
click = _click_module


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

    # Register commands from commands module
    try:
        from provide.foundation.cli.commands.deps import deps_command

        cli.add_command(deps_command)
    except ImportError:
        pass

    # Register logs commands
    try:
        from provide.foundation.cli.commands.logs import logs_group

        cli.add_command(logs_group)
    except ImportError:
        pass

    # Register OpenObserve commands if available
    try:
        from provide.foundation.integrations.openobserve.commands import (
            openobserve_group,
        )

        cli.add_command(openobserve_group)
    except ImportError:
        pass

else:

    def cli() -> None:
        """CLI stub when click is not available."""
        _require_click()


if __name__ == "__main__":
    cli()
