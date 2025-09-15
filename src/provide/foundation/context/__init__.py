"""Core context management for provide-foundation.

Provides CLI runtime context for managing command execution state,
output formatting, and CLI-specific settings.
"""

from provide.foundation.context.core import CLIContext

# Legacy compatibility
Context = CLIContext

__all__ = [
    "CLIContext",
    "Context",  # Legacy alias
]
