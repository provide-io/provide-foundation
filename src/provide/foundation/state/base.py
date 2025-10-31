#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
import contextlib
import threading
import time
from typing import Any, Generic, TypeVar

from attrs import define, field

"""Base classes for immutable state management and state machines."""

StateT = TypeVar("StateT")
EventT = TypeVar("EventT")


@define(frozen=True, slots=True, kw_only=True)
class ImmutableState:
    """Base class for immutable state objects.

    All state in Foundation should inherit from this to ensure
    immutability and provide consistent state management.
    """

    generation: int = field(default=0)
    created_at: float = field(factory=time.time)

    def with_changes(self, **changes: Any) -> ImmutableState:
        """Create a new state instance with the specified changes.

        Args:
            **changes: Field updates to apply

        Returns:
            New state instance with updated generation
        """
        # Increment generation for change tracking
        if "generation" not in changes:
            changes["generation"] = self.generation + 1

        # For attrs classes with slots, use attrs.evolve instead of __dict__
        import attrs

        return attrs.evolve(self, **changes)


@define(kw_only=True, slots=True)
class StateTransition(Generic[StateT, EventT]):
    """Represents a state transition in a state machine."""

    from_state: StateT
    event: EventT
    to_state: StateT
    guard: Callable[[], bool] | None = field(default=None)
    action: Callable[[], Any] | None = field(default=None)

    def can_transition(self) -> bool:
        """Check if transition is allowed based on guard condition."""
        return self.guard() if self.guard else True

    def execute_action(self) -> Any:
        """Execute the transition action if present."""
        return self.action() if self.action else None


class StateMachine(Generic[StateT, EventT], ABC):
    """Abstract base class for state machines.

    Provides thread-safe state transitions with guards and actions.
    """

    def __init__(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    @property
    def current_state(self) -> StateT:
        """Get the current state (thread-safe)."""
        with self._lock:
            return self._current_state

    @property
    def state_history(self) -> list[tuple[float, StateT, EventT | None]]:
        """Get the state transition history."""
        with self._lock:
            return self._state_history.copy()

    def add_transition(self, transition: StateTransition[StateT, EventT]) -> None:
        """Add a state transition to the machine."""
        key = (transition.from_state, transition.event)
        self._transitions[key] = transition

    def transition(self, event: EventT) -> bool:
        """Attempt to transition to a new state based on the event.

        Args:
            event: Event that triggers the transition

        Returns:
            True if transition was successful, False otherwise
        """
        with self._lock:
            key = (self._current_state, event)
            transition = self._transitions.get(key)

            if not transition:
                return False

            if not transition.can_transition():
                return False

            # Execute transition
            old_state = self._current_state
            self._current_state = transition.to_state

            # Record transition
            self._state_history.append((time.time(), self._current_state, event))

            # Execute action (outside lock to avoid deadlocks)
            try:
                transition.execute_action()
            except Exception:
                # If action fails, revert state
                self._current_state = old_state
                self._state_history.pop()  # Remove failed transition
                return False

            return True

    @abstractmethod
    def reset(self) -> None:
        """Reset the state machine to its initial state."""
        pass


@define(kw_only=True, slots=True)
class StateManager:
    """Thread-safe manager for immutable state objects.

    Provides atomic updates and version tracking for state objects.
    """

    _state: ImmutableState = field(alias="state")
    _lock: threading.RLock = field(factory=threading.RLock, init=False)
    _observers: list[Callable[[ImmutableState, ImmutableState], None]] = field(factory=list, init=False)

    @property
    def current_state(self) -> ImmutableState:
        """Get the current state (thread-safe)."""
        with self._lock:
            return self._state

    @property
    def generation(self) -> int:
        """Get the current state generation."""
        with self._lock:
            return self._state.generation

    def update_state(self, **changes: Any) -> ImmutableState:
        """Atomically update the state with the given changes.

        Args:
            **changes: Field updates to apply

        Returns:
            New state instance
        """
        with self._lock:
            old_state = self._state
            new_state = self._state.with_changes(**changes)
            self._state = new_state

            # Notify observers
            for observer in self._observers:
                with contextlib.suppress(Exception):
                    observer(old_state, new_state)

            return new_state

    def replace_state(self, new_state: ImmutableState) -> None:
        """Replace the entire state object.

        Args:
            new_state: New state to set
        """
        with self._lock:
            old_state = self._state
            self._state = new_state

            # Notify observers
            for observer in self._observers:
                with contextlib.suppress(Exception):
                    observer(old_state, new_state)

    def add_observer(self, observer: Callable[[ImmutableState, ImmutableState], None]) -> None:
        """Add a state change observer.

        Args:
            observer: Function called with (old_state, new_state) on changes
        """
        with self._lock:
            self._observers.append(observer)

    def remove_observer(self, observer: Callable[[ImmutableState, ImmutableState], None]) -> None:
        """Remove a state change observer.

        Args:
            observer: Observer function to remove
        """
        with self._lock, contextlib.suppress(ValueError):
            self._observers.remove(observer)


# 🧱🏗️🔚
