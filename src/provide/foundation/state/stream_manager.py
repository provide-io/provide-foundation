from __future__ import annotations

import sys
import threading
from typing import TextIO

from attrs import define, field

from provide.foundation.state.base import ImmutableState, StateManager

"""Stream manager for Foundation components - isolated to avoid circular imports."""


@define(frozen=True, slots=True)
class StreamState(ImmutableState):
    """Immutable stream state."""

    log_stream: TextIO = field(factory=lambda: sys.stderr)
    file_handle: TextIO | None = field(default=None)
    is_file_open: bool = field(default=False)
    file_path: str | None = field(default=None)


@define(kw_only=True, slots=True)
class StreamManager:
    """Thread-safe manager for stream state."""

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

    def set_file_stream(self, file_path: str, file_handle: TextIO) -> None:
        """Set the file stream."""
        with self._lock:
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