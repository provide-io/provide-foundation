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
from provide.foundation.state.transitions import (
    CircuitBreakerEvent,
    CircuitBreakerState,
    CircuitBreakerStateMachine,
)
from provide.foundation.state.logger_manager import (
    LoggerState,
    LoggerStateManager,
)

__all__ = [
    "ImmutableState",
    "StateManager",
    "StateMachine",
    "VersionedConfig",
    "ConfigManager",
    "CircuitBreakerEvent",
    "CircuitBreakerState",
    "CircuitBreakerStateMachine",
    "LoggerState",
    "LoggerStateManager",
]