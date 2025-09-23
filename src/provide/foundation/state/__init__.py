from __future__ import annotations

"""Foundation State Management.

This module provides immutable state management and state machines
for robust, thread-safe operation across Foundation components.
"""

from provide.foundation.state.base import (
    ImmutableState,
    StateManager,
    StateMachine,
)
from provide.foundation.state.config import (
    VersionedConfig,
    ConfigManager,
)

__all__ = [
    "ImmutableState",
    "StateManager",
    "StateMachine",
    "VersionedConfig",
    "ConfigManager",
]