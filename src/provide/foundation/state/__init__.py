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
from provide.foundation.state.logger_manager import (
    LoggerState,
    LoggerStateManager,
)
from provide.foundation.state.transitions import (
    CircuitBreakerEvent,
    CircuitBreakerState,
    CircuitBreakerStateMachine,
)

__all__ = [
    "CircuitBreakerEvent",
    "CircuitBreakerState",
    "CircuitBreakerStateMachine",
    "ConfigManager",
    "ImmutableState",
    "LoggerState",
    "LoggerStateManager",
    "StateMachine",
    "StateManager",
    "VersionedConfig",
]
