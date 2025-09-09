"""
Logs command group for Foundation CLI.

Provides commands for sending and querying logs with OpenTelemetry integration.
"""

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.logger import get_logger

log = get_logger(__name__)


if _HAS_CLICK:

    @click.group("logs", help="Send and query logs with OpenTelemetry integration")
    @click.pass_context
    def logs_group(ctx):
        """Logs management commands with OTEL correlation."""
        # Store shared context
        ctx.ensure_object(dict)

        # Try to get OpenObserve client if available
        try:
            from provide.foundation.integrations.openobserve import OpenObserveClient

            ctx.obj["client"] = OpenObserveClient.from_config()
        except Exception as e:
            log.debug(f"OpenObserve client not available: {e}")
            ctx.obj["client"] = None

    # Import subcommands
    from provide.foundation.cli.commands.logs.generate import (
        generate_logs_command as generate_command,
    )
    from provide.foundation.cli.commands.logs.query import query_command
    from provide.foundation.cli.commands.logs.send import send_command
    from provide.foundation.cli.commands.logs.tail import tail_command

    # Register subcommands
    logs_group.add_command(send_command)
    logs_group.add_command(query_command)
    logs_group.add_command(tail_command)
    logs_group.add_command(generate_command)

    __all__ = ["logs_group"]

else:
    # Stub when click is not available
    def logs_group(*args, **kwargs):
        """Logs command stub when click is not available."""
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )

    __all__ = []
