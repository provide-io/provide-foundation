"""Command registry management."""

from provide.foundation.registry import Registry

# Global registry for commands
_command_registry = Registry()


def get_command_registry() -> Registry:
    """Get the global command registry."""
    return _command_registry


__all__ = ["get_command_registry"]