from __future__ import annotations

import sys
import threading
from typing import TextIO

from attrs import define, field

from provide.foundation.state.base import ImmutableState, StateManager

"""State managers for Foundation components."""


@define(frozen=True, slots=True)
class StreamState(ImmutableState):
    """Immutable stream state."""

    log_stream: TextIO = field(default=sys.stderr)
    file_handle: TextIO | None = field(default=None)
    is_file_open: bool = field(default=False)
    file_path: str | None = field(default=None)


@define(kw_only=True, slots=True)
class StreamManager:
    """Thread-safe manager for stream state.

    Consolidates all stream-related state that was previously scattered
    across modules as global variables.
    """

    _state_manager: StateManager = field(alias="state_manager")
    _lock: threading.Lock = field(factory=threading.Lock, init=False)

    @classmethod
    def create_default(cls) -> StreamManager:
        """Create a StreamManager with default state."""
        initial_state = StreamState()
        state_manager = StateManager(state=initial_state)
        return cls(state_manager=state_manager)

    @property
    def current_log_stream(self) -> TextIO:
        """Get the current log stream."""
        state = self._state_manager.current_state
        if isinstance(state, StreamState):
            return state.log_stream
        return sys.stderr

    @property
    def current_file_handle(self) -> TextIO | None:
        """Get the current file handle."""
        state = self._state_manager.current_state
        if isinstance(state, StreamState):
            return state.file_handle
        return None

    @property
    def is_file_open(self) -> bool:
        """Check if a file is currently open."""
        state = self._state_manager.current_state
        if isinstance(state, StreamState):
            return state.is_file_open
        return False

    @property
    def current_file_path(self) -> str | None:
        """Get the current file path."""
        state = self._state_manager.current_state
        if isinstance(state, StreamState):
            return state.file_path
        return None

    def set_log_stream(self, stream: TextIO) -> None:
        """Set the log stream."""
        with self._lock:
            self._state_manager.update_state(log_stream=stream)

    def set_file_stream(self, file_handle: TextIO, file_path: str) -> None:
        """Set a file stream as the log destination."""
        with self._lock:
            # Close existing file if open
            current_state = self._state_manager.current_state
            if isinstance(current_state, StreamState) and current_state.file_handle:
                try:
                    if not current_state.file_handle.closed:
                        current_state.file_handle.close()
                except Exception:
                    # Don't fail on close errors
                    pass

            # Set new file stream
            self._state_manager.update_state(
                log_stream=file_handle,
                file_handle=file_handle,
                is_file_open=True,
                file_path=file_path,
            )

    def close_file_stream(self) -> None:
        """Close the current file stream and revert to stderr."""
        with self._lock:
            current_state = self._state_manager.current_state
            if isinstance(current_state, StreamState) and current_state.file_handle:
                try:
                    if not current_state.file_handle.closed:
                        current_state.file_handle.close()
                except Exception:
                    # Don't fail on close errors
                    pass

            # Revert to stderr
            self._state_manager.update_state(
                log_stream=sys.stderr,
                file_handle=None,
                is_file_open=False,
                file_path=None,
            )

    def reset_to_default(self) -> None:
        """Reset streams to default state."""
        with self._lock:
            # Close any open files first
            self.close_file_stream()

            # Reset to completely default state
            default_state = StreamState()
            self._state_manager.replace_state(default_state)


@define(frozen=True, slots=True)
class LoggerState(ImmutableState):
    """Immutable logger state."""

    setup_done: bool = field(default=False)
    setup_error: Exception | None = field(default=None)
    setup_in_progress: bool = field(default=False)
    is_configured_by_setup: bool = field(default=False)
    active_config: object | None = field(default=None)
    active_resolved_emoji_config: object | None = field(default=None)


@define(kw_only=True, slots=True)
class LoggerStateManager:
    """Thread-safe manager for logger state.

    Consolidates all logger-related state that was previously scattered
    across modules as global variables.
    """

    _state_manager: StateManager = field(alias="state_manager")
    _lock: threading.Lock = field(factory=threading.Lock, init=False)

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
            return state.is_configured_by_setup
        return False

    def mark_setup_started(self) -> None:
        """Mark setup as started."""
        with self._lock:
            self._state_manager.update_state(
                setup_in_progress=True,
                setup_error=None,
            )

    def mark_setup_completed(self, config: object | None = None, emoji_config: object | None = None) -> None:
        """Mark setup as completed."""
        with self._lock:
            self._state_manager.update_state(
                setup_done=True,
                setup_in_progress=False,
                setup_error=None,
                is_configured_by_setup=True,
                active_config=config,
                active_resolved_emoji_config=emoji_config,
            )

    def mark_setup_failed(self, error: Exception) -> None:
        """Mark setup as failed."""
        with self._lock:
            self._state_manager.update_state(
                setup_done=False,
                setup_in_progress=False,
                setup_error=error,
            )

    def reset_to_default(self) -> None:
        """Reset logger state to default."""
        with self._lock:
            default_state = LoggerState()
            self._state_manager.replace_state(default_state)
