# provide/foundation/state/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁStateMachineǁ__init____mutmut_orig(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    def xǁStateMachineǁ__init____mutmut_1(self, initial_state: StateT) -> None:
        self._current_state = None
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    def xǁStateMachineǁ__init____mutmut_2(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = None
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    def xǁStateMachineǁ__init____mutmut_3(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = None
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    def xǁStateMachineǁ__init____mutmut_4(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = None

        # Record initial state
        self._state_history.append((time.time(), initial_state, None))

    def xǁStateMachineǁ__init____mutmut_5(self, initial_state: StateT) -> None:
        self._current_state = initial_state
        self._lock = threading.RLock()
        self._transitions: dict[tuple[StateT, EventT], StateTransition[StateT, EventT]] = {}
        self._state_history: list[tuple[float, StateT, EventT | None]] = []

        # Record initial state
        self._state_history.append(None)

    xǁStateMachineǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁStateMachineǁ__init____mutmut_1": xǁStateMachineǁ__init____mutmut_1,
        "xǁStateMachineǁ__init____mutmut_2": xǁStateMachineǁ__init____mutmut_2,
        "xǁStateMachineǁ__init____mutmut_3": xǁStateMachineǁ__init____mutmut_3,
        "xǁStateMachineǁ__init____mutmut_4": xǁStateMachineǁ__init____mutmut_4,
        "xǁStateMachineǁ__init____mutmut_5": xǁStateMachineǁ__init____mutmut_5,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁStateMachineǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁStateMachineǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁStateMachineǁ__init____mutmut_orig)
    xǁStateMachineǁ__init____mutmut_orig.__name__ = "xǁStateMachineǁ__init__"

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

    def xǁStateMachineǁadd_transition__mutmut_orig(self, transition: StateTransition[StateT, EventT]) -> None:
        """Add a state transition to the machine."""
        key = (transition.from_state, transition.event)
        self._transitions[key] = transition

    def xǁStateMachineǁadd_transition__mutmut_1(self, transition: StateTransition[StateT, EventT]) -> None:
        """Add a state transition to the machine."""
        key = None
        self._transitions[key] = transition

    def xǁStateMachineǁadd_transition__mutmut_2(self, transition: StateTransition[StateT, EventT]) -> None:
        """Add a state transition to the machine."""
        key = (transition.from_state, transition.event)
        self._transitions[key] = None

    xǁStateMachineǁadd_transition__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁStateMachineǁadd_transition__mutmut_1": xǁStateMachineǁadd_transition__mutmut_1,
        "xǁStateMachineǁadd_transition__mutmut_2": xǁStateMachineǁadd_transition__mutmut_2,
    }

    def add_transition(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁStateMachineǁadd_transition__mutmut_orig"),
            object.__getattribute__(self, "xǁStateMachineǁadd_transition__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    add_transition.__signature__ = _mutmut_signature(xǁStateMachineǁadd_transition__mutmut_orig)
    xǁStateMachineǁadd_transition__mutmut_orig.__name__ = "xǁStateMachineǁadd_transition"

    def xǁStateMachineǁtransition__mutmut_orig(self, event: EventT) -> bool:
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

    def xǁStateMachineǁtransition__mutmut_1(self, event: EventT) -> bool:
        """Attempt to transition to a new state based on the event.

        Args:
            event: Event that triggers the transition

        Returns:
            True if transition was successful, False otherwise
        """
        with self._lock:
            key = None
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

    def xǁStateMachineǁtransition__mutmut_2(self, event: EventT) -> bool:
        """Attempt to transition to a new state based on the event.

        Args:
            event: Event that triggers the transition

        Returns:
            True if transition was successful, False otherwise
        """
        with self._lock:
            key = (self._current_state, event)
            transition = None

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

    def xǁStateMachineǁtransition__mutmut_3(self, event: EventT) -> bool:
        """Attempt to transition to a new state based on the event.

        Args:
            event: Event that triggers the transition

        Returns:
            True if transition was successful, False otherwise
        """
        with self._lock:
            key = (self._current_state, event)
            transition = self._transitions.get(None)

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

    def xǁStateMachineǁtransition__mutmut_4(self, event: EventT) -> bool:
        """Attempt to transition to a new state based on the event.

        Args:
            event: Event that triggers the transition

        Returns:
            True if transition was successful, False otherwise
        """
        with self._lock:
            key = (self._current_state, event)
            transition = self._transitions.get(key)

            if transition:
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

    def xǁStateMachineǁtransition__mutmut_5(self, event: EventT) -> bool:
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
                return True

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

    def xǁStateMachineǁtransition__mutmut_6(self, event: EventT) -> bool:
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

            if transition.can_transition():
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

    def xǁStateMachineǁtransition__mutmut_7(self, event: EventT) -> bool:
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
                return True

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

    def xǁStateMachineǁtransition__mutmut_8(self, event: EventT) -> bool:
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
            old_state = None
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

    def xǁStateMachineǁtransition__mutmut_9(self, event: EventT) -> bool:
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
            self._current_state = None

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

    def xǁStateMachineǁtransition__mutmut_10(self, event: EventT) -> bool:
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
            self._state_history.append(None)

            # Execute action (outside lock to avoid deadlocks)
            try:
                transition.execute_action()
            except Exception:
                # If action fails, revert state
                self._current_state = old_state
                self._state_history.pop()  # Remove failed transition
                return False

            return True

    def xǁStateMachineǁtransition__mutmut_11(self, event: EventT) -> bool:
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
                self._current_state = None
                self._state_history.pop()  # Remove failed transition
                return False

            return True

    def xǁStateMachineǁtransition__mutmut_12(self, event: EventT) -> bool:
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
                return True

            return True

    def xǁStateMachineǁtransition__mutmut_13(self, event: EventT) -> bool:
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

            return False

    xǁStateMachineǁtransition__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁStateMachineǁtransition__mutmut_1": xǁStateMachineǁtransition__mutmut_1,
        "xǁStateMachineǁtransition__mutmut_2": xǁStateMachineǁtransition__mutmut_2,
        "xǁStateMachineǁtransition__mutmut_3": xǁStateMachineǁtransition__mutmut_3,
        "xǁStateMachineǁtransition__mutmut_4": xǁStateMachineǁtransition__mutmut_4,
        "xǁStateMachineǁtransition__mutmut_5": xǁStateMachineǁtransition__mutmut_5,
        "xǁStateMachineǁtransition__mutmut_6": xǁStateMachineǁtransition__mutmut_6,
        "xǁStateMachineǁtransition__mutmut_7": xǁStateMachineǁtransition__mutmut_7,
        "xǁStateMachineǁtransition__mutmut_8": xǁStateMachineǁtransition__mutmut_8,
        "xǁStateMachineǁtransition__mutmut_9": xǁStateMachineǁtransition__mutmut_9,
        "xǁStateMachineǁtransition__mutmut_10": xǁStateMachineǁtransition__mutmut_10,
        "xǁStateMachineǁtransition__mutmut_11": xǁStateMachineǁtransition__mutmut_11,
        "xǁStateMachineǁtransition__mutmut_12": xǁStateMachineǁtransition__mutmut_12,
        "xǁStateMachineǁtransition__mutmut_13": xǁStateMachineǁtransition__mutmut_13,
    }

    def transition(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁStateMachineǁtransition__mutmut_orig"),
            object.__getattribute__(self, "xǁStateMachineǁtransition__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    transition.__signature__ = _mutmut_signature(xǁStateMachineǁtransition__mutmut_orig)
    xǁStateMachineǁtransition__mutmut_orig.__name__ = "xǁStateMachineǁtransition"

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


# <3 🧱🤝💾🪄
