from __future__ import annotations

"""Foundation State Management.

This module provides immutable state management and state machines
for robust, thread-safe operation across Foundation components.
"""

from provide.foundation.state.base import (
    ImmutableState,
    StateMachine,
    StateManager,
)
from provide.foundation.state.config import (
    ConfigManager,
    VersionedConfig,
)

__all__ = [
    "ConfigManager",
    "ImmutableState",
    "StateMachine",
    "StateManager",
    "VersionedConfig",
]
