from __future__ import annotations

from attrs import define, field

from provide.foundation.state.base import ImmutableState, StateManager

"""Logger state manager for Foundation components."""


@define(frozen=True, slots=True)
class LoggerState(ImmutableState):
    """Immutable logger state."""

    setup_done: bool = field(default=False)
    setup_in_progress: bool = field(default=False)
    setup_error: Exception | None = field(default=None)
    configured_by_setup: bool = field(default=False)


@define(kw_only=True, slots=True)
class LoggerStateManager:
    """Thread-safe manager for logger state."""

    _state_manager: StateManager = field(alias="state_manager")

    @classmethod
    def create_default(cls) -> LoggerStateManager:
        """Create a LoggerStateManager with default state."""
        initial_state = LoggerState()
        state_manager = StateManager(state=initial_state)
        return cls(state_manager=state_manager)

    @property
    def is_setup_done(self) -> bool:
        """Check if setup is complete."""
        state = self._state_manager.current_state
        if isinstance(state, LoggerState):
            return state.setup_done
        return False

    @property
    def setup_error(self) -> Exception | None:
        """Get the setup error if any."""
        state = self._state_manager.current_state
        if isinstance(state, LoggerState):
            return state.setup_error
        return None

    @property
    def is_setup_in_progress(self) -> bool:
        """Check if setup is in progress."""
        state = self._state_manager.current_state
        if isinstance(state, LoggerState):
            return state.setup_in_progress
        return False

    @property
    def is_configured_by_setup(self) -> bool:
        """Check if configured by setup."""
        state = self._state_manager.current_state
        if isinstance(state, LoggerState):
            return state.configured_by_setup
        return False

    def mark_setup_started(self) -> None:
        """Mark setup as started."""
        self._state_manager.update_state(
            setup_in_progress=True,
            setup_done=False,
            setup_error=None,
        )

    def mark_setup_completed(self) -> None:
        """Mark setup as completed."""
        self._state_manager.update_state(
            setup_done=True,
            setup_in_progress=False,
            setup_error=None,
            configured_by_setup=True,
        )

    def mark_setup_failed(self, error: Exception) -> None:
        """Mark setup as failed."""
        self._state_manager.update_state(
            setup_done=False,
            setup_in_progress=False,
            setup_error=error,
        )

    def reset_to_default(self) -> None:
        """Reset to default state."""
        default_state = LoggerState()
        self._state_manager.replace_state(default_state)
