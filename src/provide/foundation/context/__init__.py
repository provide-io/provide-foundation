from __future__ import annotations

from provide.foundation.context.core import CLIContext

"""Core context management for provide-foundation.

Provides CLI runtime context for managing command execution state,
output formatting, and CLI-specific settings.
"""

Context = CLIContext

__all__ = [
    "CLIContext",
    "Context",  # Legacy alias
]
