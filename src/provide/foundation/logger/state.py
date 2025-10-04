from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, cast

from attrs import define, field

from provide.foundation.state.base import ImmutableState, StateMachine, StateTransition

"""Logger state management using Foundation's StateMachine.

Replaces distributed state (_LAZY_SETUP_STATE dict, instance flags) with
a single, well-defined state machine.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig


class LoggerState(Enum):
    """Logger initialization states."""

    UNINITIALIZED = auto()  # Initial state
    INITIALIZING = auto()  # Setup in progress
    CONFIGURED = auto()  # Config applied successfully
    READY = auto()  # Fully initialized and operational
    ERROR = auto()  # Initialization failed


class LoggerEvent(Enum):
    """Events that trigger logger state transitions."""

    START_SETUP = auto()
    SETUP_COMPLETE = auto()
    SETUP_FAILED = auto()
    RESET = auto()


@define(frozen=True, slots=True)
class ImmutableLoggerState(ImmutableState):
    """Immutable state for logger initialization.

    Tracks configuration, setup status, and error details.
    """

    state: LoggerState = field(default=LoggerState.UNINITIALIZED)
    config: TelemetryConfig | None = field(default=None)
    error: Exception | None = field(default=None)
    setup_attempts: int = field(default=0)
    is_configured_by_setup: bool = field(default=False)


class LoggerStateMachine(StateMachine[LoggerState, LoggerEvent]):
    """State machine for managing logger initialization lifecycle.

    Provides thread-safe state transitions with guards and actions.
    """

    def __init__(self) -> None:
        """Initialize logger state machine."""
        super().__init__(initial_state=LoggerState.UNINITIALIZED)
        self._immutable_state = ImmutableLoggerState()
        self._setup_transitions()

    @property
    def immutable_state(self) -> ImmutableLoggerState:
        """Get current immutable state."""
        return self._immutable_state

    def _setup_transitions(self) -> None:
        """Define all valid state transitions."""
        # UNINITIALIZED → INITIALIZING
        self.add_transition(
            StateTransition(
                from_state=LoggerState.UNINITIALIZED,
                event=LoggerEvent.START_SETUP,
                to_state=LoggerState.INITIALIZING,
                guard=None,
                action=self._on_start_setup,
            )
        )

        # INITIALIZING → CONFIGURED
        self.add_transition(
            StateTransition(
                from_state=LoggerState.INITIALIZING,
                event=LoggerEvent.SETUP_COMPLETE,
                to_state=LoggerState.CONFIGURED,
                guard=None,
                action=self._on_setup_complete,
            )
        )

        # INITIALIZING → ERROR
        self.add_transition(
            StateTransition(
                from_state=LoggerState.INITIALIZING,
                event=LoggerEvent.SETUP_FAILED,
                to_state=LoggerState.ERROR,
                guard=None,
                action=self._on_setup_failed,
            )
        )

        # CONFIGURED → READY (transition after validation)
        self.add_transition(
            StateTransition(
                from_state=LoggerState.CONFIGURED,
                event=LoggerEvent.SETUP_COMPLETE,
                to_state=LoggerState.READY,
                guard=None,
                action=None,
            )
        )

        # Any state → UNINITIALIZED (reset)
        for state in LoggerState:
            if state != LoggerState.UNINITIALIZED:
                self.add_transition(
                    StateTransition(
                        from_state=state,
                        event=LoggerEvent.RESET,
                        to_state=LoggerState.UNINITIALIZED,
                        guard=None,
                        action=self._on_reset,
                    )
                )

    def _on_start_setup(self) -> None:
        """Handle setup start action."""
        self._immutable_state = cast(
            ImmutableLoggerState,
            self._immutable_state.with_changes(
                setup_attempts=self._immutable_state.setup_attempts + 1
            ),
        )

    def _on_setup_complete(self) -> None:
        """Handle setup completion action."""
        self._immutable_state = cast(
            ImmutableLoggerState,
            self._immutable_state.with_changes(is_configured_by_setup=True),
        )

    def _on_setup_failed(self) -> None:
        """Handle setup failure action."""
        # Error details should be set via set_error() before triggering transition
        pass

    def _on_reset(self) -> None:
        """Handle reset action."""
        self._immutable_state = ImmutableLoggerState()

    def reset(self) -> None:
        """Reset state machine to initial state."""
        self.transition(LoggerEvent.RESET)

    def set_config(self, config: TelemetryConfig) -> None:
        """Set configuration (can be called during setup)."""
        self._immutable_state = cast(
            ImmutableLoggerState,
            self._immutable_state.with_changes(config=config),
        )

    def set_error(self, error: Exception) -> None:
        """Set error details (call before transitioning to ERROR state)."""
        self._immutable_state = cast(
            ImmutableLoggerState,
            self._immutable_state.with_changes(error=error),
        )

    @property
    def is_ready(self) -> bool:
        """Check if logger is ready."""
        return self.current_state in (LoggerState.CONFIGURED, LoggerState.READY)

    @property
    def is_initializing(self) -> bool:
        """Check if setup is in progress."""
        return self.current_state == LoggerState.INITIALIZING

    @property
    def has_error(self) -> bool:
        """Check if logger has encountered an error."""
        return self.current_state == LoggerState.ERROR or self._immutable_state.error is not None

    @property
    def config(self) -> TelemetryConfig | None:
        """Get current configuration."""
        return self._immutable_state.config
