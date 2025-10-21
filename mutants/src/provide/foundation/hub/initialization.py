# provide/foundation/hub/initialization.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import contextlib
from enum import Enum, auto
import threading
from typing import Any

from attrs import define

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.errors.runtime import RuntimeError as FoundationRuntimeError
from provide.foundation.state.base import ImmutableState, StateMachine, StateTransition

"""Simplified, centralized initialization coordinator.

This module consolidates all initialization logic into a single,
thread-safe state machine that uses the LockManager for coordination.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class InitState(Enum):
    """Initialization states."""

    UNINITIALIZED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    FAILED = auto()


class InitEvent(Enum):
    """Initialization events."""

    START = auto()
    COMPLETE = auto()
    FAIL = auto()
    RESET = auto()


@define(frozen=True, slots=True, kw_only=True)
class InitializationState(ImmutableState):
    """Immutable initialization state."""

    status: InitState = InitState.UNINITIALIZED
    config: Any = None
    logger_instance: Any = None
    error: Exception | None = None


class InitializationStateMachine(StateMachine[InitState, InitEvent]):
    """State machine for Foundation initialization.

    States:
    - UNINITIALIZED: Initial state, no initialization attempted
    - INITIALIZING: Initialization in progress
    - INITIALIZED: Successfully initialized
    - FAILED: Initialization failed

    Events:
    - START: Begin initialization
    - COMPLETE: Mark initialization complete
    - FAIL: Mark initialization failed
    - RESET: Reset to uninitialized state
    """

    def xǁInitializationStateMachineǁ__init____mutmut_orig(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_1(self) -> None:
        """Initialize the state machine."""
        super().__init__(None)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_2(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = None
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_3(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = None

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_4(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            None
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_5(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=None,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_6(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=None,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_7(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=None,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_8(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_9(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_10(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_11(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            None
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_12(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=None,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_13(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=None,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_14(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=None,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_15(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=None,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_16(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_17(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_18(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_19(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_20(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            None
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_21(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=None,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_22(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=None,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_23(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=None,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_24(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=None,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_25(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_26(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_27(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_28(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_29(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                None
            )

    def xǁInitializationStateMachineǁ__init____mutmut_30(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=None,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_31(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=None,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_32(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=None,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_33(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=None,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_34(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_35(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    to_state=InitState.UNINITIALIZED,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_36(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    action=self._event.clear,
                )
            )

    def xǁInitializationStateMachineǁ__init____mutmut_37(self) -> None:
        """Initialize the state machine."""
        super().__init__(InitState.UNINITIALIZED)
        self._state_data = InitializationState()
        self._event = threading.Event()

        # Define transitions
        self.add_transition(
            StateTransition(
                from_state=InitState.UNINITIALIZED,
                event=InitEvent.START,
                to_state=InitState.INITIALIZING,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.COMPLETE,
                to_state=InitState.INITIALIZED,
                action=self._event.set,
            )
        )
        self.add_transition(
            StateTransition(
                from_state=InitState.INITIALIZING,
                event=InitEvent.FAIL,
                to_state=InitState.FAILED,
                action=self._event.set,
            )
        )
        # Allow reset from any state
        for state in [InitState.INITIALIZED, InitState.FAILED, InitState.INITIALIZING]:
            self.add_transition(
                StateTransition(
                    from_state=state,
                    event=InitEvent.RESET,
                    to_state=InitState.UNINITIALIZED,
                    )
            )
    
    xǁInitializationStateMachineǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationStateMachineǁ__init____mutmut_1': xǁInitializationStateMachineǁ__init____mutmut_1, 
        'xǁInitializationStateMachineǁ__init____mutmut_2': xǁInitializationStateMachineǁ__init____mutmut_2, 
        'xǁInitializationStateMachineǁ__init____mutmut_3': xǁInitializationStateMachineǁ__init____mutmut_3, 
        'xǁInitializationStateMachineǁ__init____mutmut_4': xǁInitializationStateMachineǁ__init____mutmut_4, 
        'xǁInitializationStateMachineǁ__init____mutmut_5': xǁInitializationStateMachineǁ__init____mutmut_5, 
        'xǁInitializationStateMachineǁ__init____mutmut_6': xǁInitializationStateMachineǁ__init____mutmut_6, 
        'xǁInitializationStateMachineǁ__init____mutmut_7': xǁInitializationStateMachineǁ__init____mutmut_7, 
        'xǁInitializationStateMachineǁ__init____mutmut_8': xǁInitializationStateMachineǁ__init____mutmut_8, 
        'xǁInitializationStateMachineǁ__init____mutmut_9': xǁInitializationStateMachineǁ__init____mutmut_9, 
        'xǁInitializationStateMachineǁ__init____mutmut_10': xǁInitializationStateMachineǁ__init____mutmut_10, 
        'xǁInitializationStateMachineǁ__init____mutmut_11': xǁInitializationStateMachineǁ__init____mutmut_11, 
        'xǁInitializationStateMachineǁ__init____mutmut_12': xǁInitializationStateMachineǁ__init____mutmut_12, 
        'xǁInitializationStateMachineǁ__init____mutmut_13': xǁInitializationStateMachineǁ__init____mutmut_13, 
        'xǁInitializationStateMachineǁ__init____mutmut_14': xǁInitializationStateMachineǁ__init____mutmut_14, 
        'xǁInitializationStateMachineǁ__init____mutmut_15': xǁInitializationStateMachineǁ__init____mutmut_15, 
        'xǁInitializationStateMachineǁ__init____mutmut_16': xǁInitializationStateMachineǁ__init____mutmut_16, 
        'xǁInitializationStateMachineǁ__init____mutmut_17': xǁInitializationStateMachineǁ__init____mutmut_17, 
        'xǁInitializationStateMachineǁ__init____mutmut_18': xǁInitializationStateMachineǁ__init____mutmut_18, 
        'xǁInitializationStateMachineǁ__init____mutmut_19': xǁInitializationStateMachineǁ__init____mutmut_19, 
        'xǁInitializationStateMachineǁ__init____mutmut_20': xǁInitializationStateMachineǁ__init____mutmut_20, 
        'xǁInitializationStateMachineǁ__init____mutmut_21': xǁInitializationStateMachineǁ__init____mutmut_21, 
        'xǁInitializationStateMachineǁ__init____mutmut_22': xǁInitializationStateMachineǁ__init____mutmut_22, 
        'xǁInitializationStateMachineǁ__init____mutmut_23': xǁInitializationStateMachineǁ__init____mutmut_23, 
        'xǁInitializationStateMachineǁ__init____mutmut_24': xǁInitializationStateMachineǁ__init____mutmut_24, 
        'xǁInitializationStateMachineǁ__init____mutmut_25': xǁInitializationStateMachineǁ__init____mutmut_25, 
        'xǁInitializationStateMachineǁ__init____mutmut_26': xǁInitializationStateMachineǁ__init____mutmut_26, 
        'xǁInitializationStateMachineǁ__init____mutmut_27': xǁInitializationStateMachineǁ__init____mutmut_27, 
        'xǁInitializationStateMachineǁ__init____mutmut_28': xǁInitializationStateMachineǁ__init____mutmut_28, 
        'xǁInitializationStateMachineǁ__init____mutmut_29': xǁInitializationStateMachineǁ__init____mutmut_29, 
        'xǁInitializationStateMachineǁ__init____mutmut_30': xǁInitializationStateMachineǁ__init____mutmut_30, 
        'xǁInitializationStateMachineǁ__init____mutmut_31': xǁInitializationStateMachineǁ__init____mutmut_31, 
        'xǁInitializationStateMachineǁ__init____mutmut_32': xǁInitializationStateMachineǁ__init____mutmut_32, 
        'xǁInitializationStateMachineǁ__init____mutmut_33': xǁInitializationStateMachineǁ__init____mutmut_33, 
        'xǁInitializationStateMachineǁ__init____mutmut_34': xǁInitializationStateMachineǁ__init____mutmut_34, 
        'xǁInitializationStateMachineǁ__init____mutmut_35': xǁInitializationStateMachineǁ__init____mutmut_35, 
        'xǁInitializationStateMachineǁ__init____mutmut_36': xǁInitializationStateMachineǁ__init____mutmut_36, 
        'xǁInitializationStateMachineǁ__init____mutmut_37': xǁInitializationStateMachineǁ__init____mutmut_37
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationStateMachineǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInitializationStateMachineǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInitializationStateMachineǁ__init____mutmut_orig)
    xǁInitializationStateMachineǁ__init____mutmut_orig.__name__ = 'xǁInitializationStateMachineǁ__init__'

    @property
    def state_data(self) -> InitializationState:
        """Get the current state data."""
        with self._lock:
            return self._state_data

    def xǁInitializationStateMachineǁmark_complete__mutmut_orig(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_1(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = None
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_2(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=None,
                config=config,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_3(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=None,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_4(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                logger_instance=None,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_5(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                config=config,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_6(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_7(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                error=None,
            )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_8(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                logger_instance=logger_instance,
                )
        self.transition(InitEvent.COMPLETE)

    def xǁInitializationStateMachineǁmark_complete__mutmut_9(self, config: Any, logger_instance: Any) -> None:
        """Mark initialization as complete."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.INITIALIZED,
                config=config,
                logger_instance=logger_instance,
                error=None,
            )
        self.transition(None)
    
    xǁInitializationStateMachineǁmark_complete__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationStateMachineǁmark_complete__mutmut_1': xǁInitializationStateMachineǁmark_complete__mutmut_1, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_2': xǁInitializationStateMachineǁmark_complete__mutmut_2, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_3': xǁInitializationStateMachineǁmark_complete__mutmut_3, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_4': xǁInitializationStateMachineǁmark_complete__mutmut_4, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_5': xǁInitializationStateMachineǁmark_complete__mutmut_5, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_6': xǁInitializationStateMachineǁmark_complete__mutmut_6, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_7': xǁInitializationStateMachineǁmark_complete__mutmut_7, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_8': xǁInitializationStateMachineǁmark_complete__mutmut_8, 
        'xǁInitializationStateMachineǁmark_complete__mutmut_9': xǁInitializationStateMachineǁmark_complete__mutmut_9
    }
    
    def mark_complete(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationStateMachineǁmark_complete__mutmut_orig"), object.__getattribute__(self, "xǁInitializationStateMachineǁmark_complete__mutmut_mutants"), args, kwargs, self)
        return result 
    
    mark_complete.__signature__ = _mutmut_signature(xǁInitializationStateMachineǁmark_complete__mutmut_orig)
    xǁInitializationStateMachineǁmark_complete__mutmut_orig.__name__ = 'xǁInitializationStateMachineǁmark_complete'

    def xǁInitializationStateMachineǁmark_failed__mutmut_orig(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.FAILED,
                error=error,
            )
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_1(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = None
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_2(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=None,
                error=error,
            )
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_3(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.FAILED,
                error=None,
            )
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_4(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                error=error,
            )
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_5(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.FAILED,
                )
        self.transition(InitEvent.FAIL)

    def xǁInitializationStateMachineǁmark_failed__mutmut_6(self, error: Exception) -> None:
        """Mark initialization as failed."""
        with self._lock:
            # Type ignore needed because with_changes returns ImmutableState
            # but we know it's actually InitializationState
            self._state_data = self._state_data.with_changes(  # type: ignore[assignment]
                status=InitState.FAILED,
                error=error,
            )
        self.transition(None)
    
    xǁInitializationStateMachineǁmark_failed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationStateMachineǁmark_failed__mutmut_1': xǁInitializationStateMachineǁmark_failed__mutmut_1, 
        'xǁInitializationStateMachineǁmark_failed__mutmut_2': xǁInitializationStateMachineǁmark_failed__mutmut_2, 
        'xǁInitializationStateMachineǁmark_failed__mutmut_3': xǁInitializationStateMachineǁmark_failed__mutmut_3, 
        'xǁInitializationStateMachineǁmark_failed__mutmut_4': xǁInitializationStateMachineǁmark_failed__mutmut_4, 
        'xǁInitializationStateMachineǁmark_failed__mutmut_5': xǁInitializationStateMachineǁmark_failed__mutmut_5, 
        'xǁInitializationStateMachineǁmark_failed__mutmut_6': xǁInitializationStateMachineǁmark_failed__mutmut_6
    }
    
    def mark_failed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationStateMachineǁmark_failed__mutmut_orig"), object.__getattribute__(self, "xǁInitializationStateMachineǁmark_failed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    mark_failed.__signature__ = _mutmut_signature(xǁInitializationStateMachineǁmark_failed__mutmut_orig)
    xǁInitializationStateMachineǁmark_failed__mutmut_orig.__name__ = 'xǁInitializationStateMachineǁmark_failed'

    def xǁInitializationStateMachineǁwait_for_completion__mutmut_orig(self, timeout: float = 10.0) -> bool:
        """Wait for initialization to complete."""
        return self._event.wait(timeout)

    def xǁInitializationStateMachineǁwait_for_completion__mutmut_1(self, timeout: float = 11.0) -> bool:
        """Wait for initialization to complete."""
        return self._event.wait(timeout)

    def xǁInitializationStateMachineǁwait_for_completion__mutmut_2(self, timeout: float = 10.0) -> bool:
        """Wait for initialization to complete."""
        return self._event.wait(None)
    
    xǁInitializationStateMachineǁwait_for_completion__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationStateMachineǁwait_for_completion__mutmut_1': xǁInitializationStateMachineǁwait_for_completion__mutmut_1, 
        'xǁInitializationStateMachineǁwait_for_completion__mutmut_2': xǁInitializationStateMachineǁwait_for_completion__mutmut_2
    }
    
    def wait_for_completion(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationStateMachineǁwait_for_completion__mutmut_orig"), object.__getattribute__(self, "xǁInitializationStateMachineǁwait_for_completion__mutmut_mutants"), args, kwargs, self)
        return result 
    
    wait_for_completion.__signature__ = _mutmut_signature(xǁInitializationStateMachineǁwait_for_completion__mutmut_orig)
    xǁInitializationStateMachineǁwait_for_completion__mutmut_orig.__name__ = 'xǁInitializationStateMachineǁwait_for_completion'

    def xǁInitializationStateMachineǁreset__mutmut_orig(self) -> None:
        """Reset the state machine to uninitialized."""
        with self._lock:
            self._state_data = InitializationState()
        self.transition(InitEvent.RESET)

    def xǁInitializationStateMachineǁreset__mutmut_1(self) -> None:
        """Reset the state machine to uninitialized."""
        with self._lock:
            self._state_data = None
        self.transition(InitEvent.RESET)

    def xǁInitializationStateMachineǁreset__mutmut_2(self) -> None:
        """Reset the state machine to uninitialized."""
        with self._lock:
            self._state_data = InitializationState()
        self.transition(None)
    
    xǁInitializationStateMachineǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationStateMachineǁreset__mutmut_1': xǁInitializationStateMachineǁreset__mutmut_1, 
        'xǁInitializationStateMachineǁreset__mutmut_2': xǁInitializationStateMachineǁreset__mutmut_2
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationStateMachineǁreset__mutmut_orig"), object.__getattribute__(self, "xǁInitializationStateMachineǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁInitializationStateMachineǁreset__mutmut_orig)
    xǁInitializationStateMachineǁreset__mutmut_orig.__name__ = 'xǁInitializationStateMachineǁreset'


class InitializationCoordinator:
    """Centralized initialization coordinator using state machine."""

    def xǁInitializationCoordinatorǁ__init____mutmut_orig(self) -> None:
        """Initialize coordinator."""
        self._state_machine = InitializationStateMachine()
        self._lock_manager = get_lock_manager()

        # Register all foundation locks (includes coordinator lock)
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            register_foundation_locks()

    def xǁInitializationCoordinatorǁ__init____mutmut_1(self) -> None:
        """Initialize coordinator."""
        self._state_machine = None
        self._lock_manager = get_lock_manager()

        # Register all foundation locks (includes coordinator lock)
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            register_foundation_locks()

    def xǁInitializationCoordinatorǁ__init____mutmut_2(self) -> None:
        """Initialize coordinator."""
        self._state_machine = InitializationStateMachine()
        self._lock_manager = None

        # Register all foundation locks (includes coordinator lock)
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(ValueError):
            # Already registered if ValueError raised
            register_foundation_locks()

    def xǁInitializationCoordinatorǁ__init____mutmut_3(self) -> None:
        """Initialize coordinator."""
        self._state_machine = InitializationStateMachine()
        self._lock_manager = get_lock_manager()

        # Register all foundation locks (includes coordinator lock)
        from provide.foundation.concurrency.locks import register_foundation_locks

        with contextlib.suppress(None):
            # Already registered if ValueError raised
            register_foundation_locks()
    
    xǁInitializationCoordinatorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁ__init____mutmut_1': xǁInitializationCoordinatorǁ__init____mutmut_1, 
        'xǁInitializationCoordinatorǁ__init____mutmut_2': xǁInitializationCoordinatorǁ__init____mutmut_2, 
        'xǁInitializationCoordinatorǁ__init____mutmut_3': xǁInitializationCoordinatorǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁ__init____mutmut_orig)
    xǁInitializationCoordinatorǁ__init____mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁ__init__'

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_orig(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_1(self, registry: Any, config: Any = None, force: bool = True) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_2(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = None
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_3(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED or not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_4(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state != InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_5(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_6(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire(None):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_7(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("XXfoundation.init.coordinatorXX"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_8(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("FOUNDATION.INIT.COORDINATOR"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_9(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = None
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_10(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED or not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_11(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state != InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_12(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_13(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(None)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_14(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = None

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_15(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(None, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_16(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, None):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_17(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block("Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_18(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, ):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_19(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "XXFoundation config initializationXX"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_20(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_21(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "FOUNDATION CONFIG INITIALIZATION"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_22(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = None

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_23(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(None)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_24(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(None, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_25(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, None):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_26(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block("Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_27(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, ):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_28(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "XXFoundation logger initializationXX"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_29(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_30(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "FOUNDATION LOGGER INITIALIZATION"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_31(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = None

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_32(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(None, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_33(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, None)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_34(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_35(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, )

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_36(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(None, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_37(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, None):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_38(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block("Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_39(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, ):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_40(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "XXFoundation component registrationXX"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_41(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_42(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "FOUNDATION COMPONENT REGISTRATION"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_43(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(None, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_44(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, None, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_45(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, None)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_46(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_47(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_48(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, )

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_49(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(None, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_50(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, None):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_51(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block("Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_52(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, ):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_53(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "XXFoundation event handler setupXX"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_54(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_55(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "FOUNDATION EVENT HANDLER SETUP"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_56(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(None, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_57(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, None)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_58(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_59(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, )

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_60(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(None)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_61(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    None,
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_62(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code=None,
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_63(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=None,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_64(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase=None,
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_65(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_66(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_67(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_68(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_69(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="XXFOUNDATION_INIT_FAILEDXX",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_70(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="foundation_init_failed",
                    cause=e,
                    initialization_phase="config_and_logger",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_71(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="XXconfig_and_loggerXX",
                ) from e

    def xǁInitializationCoordinatorǁinitialize_foundation__mutmut_72(self, registry: Any, config: Any = None, force: bool = False) -> tuple[Any, Any]:
        """Simplified, single-path initialization.

        Args:
            registry: Component registry
            config: Optional configuration
            force: Force re-initialization

        Returns:
            Tuple of (config, logger_instance)

        Raises:
            RuntimeError: If initialization fails
        """
        # Fast path if already initialized and not forcing
        state_data = self._state_machine.state_data
        if self._state_machine.current_state == InitState.INITIALIZED and not force:
            return state_data.config, state_data.logger_instance

        # Use lock manager for thread-safe initialization
        with self._lock_manager.acquire("foundation.init.coordinator"):
            # Double-check after acquiring lock
            state_data = self._state_machine.state_data
            if self._state_machine.current_state == InitState.INITIALIZED and not force:
                return state_data.config, state_data.logger_instance

            if force:
                self._state_machine.reset()

            # Transition to INITIALIZING state
            self._state_machine.transition(InitEvent.START)

            try:
                # Get foundation internal logger for timing
                from provide.foundation.logger.setup.coordinator import (
                    create_foundation_internal_logger,
                )
                from provide.foundation.utils.timing import timed_block

                setup_logger = create_foundation_internal_logger()

                # Single initialization path with performance monitoring
                with timed_block(setup_logger, "Foundation config initialization"):
                    actual_config = self._initialize_config(config)

                with timed_block(setup_logger, "Foundation logger initialization"):
                    logger_instance = self._initialize_logger(actual_config, registry)

                with timed_block(setup_logger, "Foundation component registration"):
                    # Register with registry
                    self._register_components(registry, actual_config, logger_instance)

                with timed_block(setup_logger, "Foundation event handler setup"):
                    # Set up event handlers
                    self._setup_event_handlers()

                # Mark complete (transitions to INITIALIZED)
                self._state_machine.mark_complete(actual_config, logger_instance)

                return actual_config, logger_instance

            except Exception as e:
                self._state_machine.mark_failed(e)
                raise FoundationRuntimeError(
                    f"Foundation initialization failed: {e}",
                    code="FOUNDATION_INIT_FAILED",
                    cause=e,
                    initialization_phase="CONFIG_AND_LOGGER",
                ) from e
    
    xǁInitializationCoordinatorǁinitialize_foundation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_1': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_1, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_2': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_2, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_3': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_3, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_4': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_4, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_5': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_5, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_6': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_6, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_7': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_7, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_8': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_8, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_9': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_9, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_10': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_10, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_11': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_11, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_12': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_12, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_13': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_13, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_14': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_14, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_15': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_15, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_16': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_16, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_17': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_17, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_18': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_18, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_19': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_19, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_20': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_20, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_21': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_21, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_22': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_22, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_23': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_23, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_24': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_24, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_25': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_25, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_26': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_26, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_27': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_27, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_28': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_28, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_29': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_29, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_30': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_30, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_31': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_31, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_32': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_32, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_33': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_33, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_34': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_34, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_35': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_35, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_36': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_36, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_37': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_37, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_38': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_38, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_39': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_39, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_40': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_40, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_41': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_41, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_42': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_42, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_43': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_43, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_44': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_44, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_45': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_45, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_46': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_46, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_47': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_47, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_48': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_48, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_49': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_49, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_50': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_50, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_51': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_51, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_52': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_52, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_53': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_53, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_54': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_54, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_55': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_55, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_56': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_56, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_57': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_57, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_58': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_58, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_59': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_59, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_60': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_60, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_61': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_61, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_62': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_62, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_63': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_63, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_64': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_64, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_65': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_65, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_66': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_66, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_67': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_67, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_68': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_68, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_69': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_69, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_70': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_70, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_71': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_71, 
        'xǁInitializationCoordinatorǁinitialize_foundation__mutmut_72': xǁInitializationCoordinatorǁinitialize_foundation__mutmut_72
    }
    
    def initialize_foundation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁinitialize_foundation__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁinitialize_foundation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    initialize_foundation.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁinitialize_foundation__mutmut_orig)
    xǁInitializationCoordinatorǁinitialize_foundation__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁinitialize_foundation'

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_orig(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_1(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = None

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_2(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None or getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_3(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED or state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_4(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state != InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_5(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_6(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(None, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_7(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, None, "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_8(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", None) is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_9(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr("service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_10(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_11(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", ) is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_12(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "XXservice_nameXX", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_13(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "SERVICE_NAME", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_14(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "XXnot-noneXX") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_15(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "NOT-NONE") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_16(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is not None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_17(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = None  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_18(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=None)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_19(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name=None,
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_20(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=None,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_21(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension=None,
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_22(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata=None,
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_23(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=None,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_24(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_25(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_26(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_27(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_28(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_29(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="XXfoundation.configXX",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_30(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="FOUNDATION.CONFIG",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_31(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="XXsingletonXX",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_32(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="SINGLETON",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_33(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"XXinitializedXX": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_34(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"INITIALIZED": True},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_35(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": False},
                replace=True,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_36(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=False,
            )

            return True

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_37(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return False

        return False

    def xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_38(self, registry: Any, new_config: Any) -> bool:
        """Update config in-place if current config is from auto-init (service_name=None).

        This provides a lightweight alternative to force re-initialization when
        applications want to override default auto-init config with explicit config.

        Args:
            registry: Component registry
            new_config: New configuration to use

        Returns:
            True if config was updated, False if no update needed
        """
        state_data = self._state_machine.state_data

        # Only update if initialized and current config has no service_name (auto-init indicator)
        if (
            self._state_machine.current_state == InitState.INITIALIZED
            and state_data.config is not None
            and getattr(state_data.config, "service_name", "not-none") is None
        ):
            # Update state machine config
            with self._state_machine._lock:
                self._state_machine._state_data = state_data.with_changes(config=new_config)  # type: ignore[assignment]

            # Update registry config
            registry.register(
                name="foundation.config",
                value=new_config,
                dimension="singleton",
                metadata={"initialized": True},
                replace=True,
            )

            return True

        return True
    
    xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_1': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_1, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_2': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_2, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_3': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_3, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_4': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_4, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_5': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_5, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_6': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_6, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_7': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_7, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_8': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_8, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_9': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_9, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_10': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_10, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_11': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_11, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_12': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_12, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_13': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_13, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_14': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_14, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_15': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_15, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_16': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_16, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_17': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_17, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_18': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_18, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_19': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_19, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_20': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_20, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_21': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_21, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_22': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_22, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_23': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_23, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_24': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_24, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_25': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_25, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_26': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_26, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_27': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_27, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_28': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_28, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_29': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_29, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_30': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_30, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_31': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_31, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_32': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_32, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_33': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_33, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_34': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_34, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_35': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_35, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_36': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_36, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_37': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_37, 
        'xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_38': xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_38
    }
    
    def update_config_if_default(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update_config_if_default.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_orig)
    xǁInitializationCoordinatorǁupdate_config_if_default__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁupdate_config_if_default'

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_orig(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "import" in str(e).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_1(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "XXimportXX" in str(e).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_2(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "IMPORT" in str(e).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_3(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "import" not in str(e).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_4(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "import" in str(e).upper():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()

    def xǁInitializationCoordinatorǁ_initialize_config__mutmut_5(self, config: Any) -> Any:
        """Initialize configuration."""
        if config:
            return config

        # Load from environment
        from provide.foundation.logger.config import TelemetryConfig

        try:
            return TelemetryConfig.from_env()
        except Exception as e:
            # Only fallback for config parsing errors, not import errors
            if "import" in str(None).lower():
                raise
            # Fallback to minimal config for environment parsing issues
            return TelemetryConfig()
    
    xǁInitializationCoordinatorǁ_initialize_config__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁ_initialize_config__mutmut_1': xǁInitializationCoordinatorǁ_initialize_config__mutmut_1, 
        'xǁInitializationCoordinatorǁ_initialize_config__mutmut_2': xǁInitializationCoordinatorǁ_initialize_config__mutmut_2, 
        'xǁInitializationCoordinatorǁ_initialize_config__mutmut_3': xǁInitializationCoordinatorǁ_initialize_config__mutmut_3, 
        'xǁInitializationCoordinatorǁ_initialize_config__mutmut_4': xǁInitializationCoordinatorǁ_initialize_config__mutmut_4, 
        'xǁInitializationCoordinatorǁ_initialize_config__mutmut_5': xǁInitializationCoordinatorǁ_initialize_config__mutmut_5
    }
    
    def _initialize_config(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁ_initialize_config__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁ_initialize_config__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _initialize_config.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁ_initialize_config__mutmut_orig)
    xǁInitializationCoordinatorǁ_initialize_config__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁ_initialize_config'

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_orig(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_1(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = None

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_2(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type(None, (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_3(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", None, {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_4(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), None)()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_5(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type((), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_6(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_7(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), )()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_8(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("XXHubWrapperXX", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_9(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("hubwrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_10(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HUBWRAPPER", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_11(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"XX_component_registryXX": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_12(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_COMPONENT_REGISTRY": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_13(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "XX_foundation_configXX": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_14(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_FOUNDATION_CONFIG": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_15(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = None
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_16(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=None)
        logger_instance.setup(config)

        return logger_instance

    def xǁInitializationCoordinatorǁ_initialize_logger__mutmut_17(self, config: Any, registry: Any) -> Any:
        """Initialize logger instance."""
        from provide.foundation.logger.core import FoundationLogger

        # Create hub wrapper for logger
        hub_wrapper = type("HubWrapper", (), {"_component_registry": registry, "_foundation_config": config})()

        logger_instance = FoundationLogger(hub=hub_wrapper)
        logger_instance.setup(None)

        return logger_instance
    
    xǁInitializationCoordinatorǁ_initialize_logger__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_1': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_1, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_2': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_2, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_3': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_3, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_4': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_4, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_5': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_5, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_6': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_6, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_7': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_7, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_8': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_8, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_9': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_9, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_10': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_10, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_11': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_11, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_12': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_12, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_13': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_13, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_14': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_14, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_15': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_15, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_16': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_16, 
        'xǁInitializationCoordinatorǁ_initialize_logger__mutmut_17': xǁInitializationCoordinatorǁ_initialize_logger__mutmut_17
    }
    
    def _initialize_logger(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁ_initialize_logger__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁ_initialize_logger__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _initialize_logger.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁ_initialize_logger__mutmut_orig)
    xǁInitializationCoordinatorǁ_initialize_logger__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁ_initialize_logger'

    def xǁInitializationCoordinatorǁ_register_components__mutmut_orig(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_1(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name=None,
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_2(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=None,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_3(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension=None,
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_4(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata=None,
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_5(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=None,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_6(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_7(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_8(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_9(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_10(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_11(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="XXfoundation.configXX",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_12(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="FOUNDATION.CONFIG",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_13(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="XXsingletonXX",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_14(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="SINGLETON",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_15(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"XXinitializedXX": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_16(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"INITIALIZED": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_17(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": False},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_18(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=False,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_19(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name=None,
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_20(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=None,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_21(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension=None,
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_22(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata=None,
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_23(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=None,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_24(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_25(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_26(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_27(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_28(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_29(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="XXfoundation.logger.instanceXX",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_30(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="FOUNDATION.LOGGER.INSTANCE",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_31(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="XXsingletonXX",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_32(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="SINGLETON",
            metadata={"initialized": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_33(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"XXinitializedXX": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_34(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"INITIALIZED": True},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_35(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": False},
            replace=True,
        )

    def xǁInitializationCoordinatorǁ_register_components__mutmut_36(self, registry: Any, config: Any, logger_instance: Any) -> None:
        """Register components in registry."""
        # Register config
        registry.register(
            name="foundation.config",
            value=config,
            dimension="singleton",
            metadata={"initialized": True},
            replace=True,
        )

        # Register logger
        registry.register(
            name="foundation.logger.instance",
            value=logger_instance,
            dimension="singleton",
            metadata={"initialized": True},
            replace=False,
        )
    
    xǁInitializationCoordinatorǁ_register_components__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁ_register_components__mutmut_1': xǁInitializationCoordinatorǁ_register_components__mutmut_1, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_2': xǁInitializationCoordinatorǁ_register_components__mutmut_2, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_3': xǁInitializationCoordinatorǁ_register_components__mutmut_3, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_4': xǁInitializationCoordinatorǁ_register_components__mutmut_4, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_5': xǁInitializationCoordinatorǁ_register_components__mutmut_5, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_6': xǁInitializationCoordinatorǁ_register_components__mutmut_6, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_7': xǁInitializationCoordinatorǁ_register_components__mutmut_7, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_8': xǁInitializationCoordinatorǁ_register_components__mutmut_8, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_9': xǁInitializationCoordinatorǁ_register_components__mutmut_9, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_10': xǁInitializationCoordinatorǁ_register_components__mutmut_10, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_11': xǁInitializationCoordinatorǁ_register_components__mutmut_11, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_12': xǁInitializationCoordinatorǁ_register_components__mutmut_12, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_13': xǁInitializationCoordinatorǁ_register_components__mutmut_13, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_14': xǁInitializationCoordinatorǁ_register_components__mutmut_14, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_15': xǁInitializationCoordinatorǁ_register_components__mutmut_15, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_16': xǁInitializationCoordinatorǁ_register_components__mutmut_16, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_17': xǁInitializationCoordinatorǁ_register_components__mutmut_17, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_18': xǁInitializationCoordinatorǁ_register_components__mutmut_18, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_19': xǁInitializationCoordinatorǁ_register_components__mutmut_19, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_20': xǁInitializationCoordinatorǁ_register_components__mutmut_20, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_21': xǁInitializationCoordinatorǁ_register_components__mutmut_21, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_22': xǁInitializationCoordinatorǁ_register_components__mutmut_22, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_23': xǁInitializationCoordinatorǁ_register_components__mutmut_23, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_24': xǁInitializationCoordinatorǁ_register_components__mutmut_24, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_25': xǁInitializationCoordinatorǁ_register_components__mutmut_25, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_26': xǁInitializationCoordinatorǁ_register_components__mutmut_26, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_27': xǁInitializationCoordinatorǁ_register_components__mutmut_27, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_28': xǁInitializationCoordinatorǁ_register_components__mutmut_28, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_29': xǁInitializationCoordinatorǁ_register_components__mutmut_29, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_30': xǁInitializationCoordinatorǁ_register_components__mutmut_30, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_31': xǁInitializationCoordinatorǁ_register_components__mutmut_31, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_32': xǁInitializationCoordinatorǁ_register_components__mutmut_32, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_33': xǁInitializationCoordinatorǁ_register_components__mutmut_33, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_34': xǁInitializationCoordinatorǁ_register_components__mutmut_34, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_35': xǁInitializationCoordinatorǁ_register_components__mutmut_35, 
        'xǁInitializationCoordinatorǁ_register_components__mutmut_36': xǁInitializationCoordinatorǁ_register_components__mutmut_36
    }
    
    def _register_components(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁ_register_components__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁ_register_components__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _register_components.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁ_register_components__mutmut_orig)
    xǁInitializationCoordinatorǁ_register_components__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁ_register_components'

    def _setup_event_handlers(self) -> None:
        """Set up event handlers."""
        try:
            from provide.foundation.hub.event_handlers import setup_event_logging

            setup_event_logging()
        except Exception:
            # If event handler setup fails, continue without it
            pass

    def get_state(self) -> InitializationState:
        """Get current initialization state."""
        return self._state_machine.state_data

    def xǁInitializationCoordinatorǁis_initialized__mutmut_orig(self) -> bool:
        """Check if foundation is initialized."""
        return self._state_machine.current_state == InitState.INITIALIZED

    def xǁInitializationCoordinatorǁis_initialized__mutmut_1(self) -> bool:
        """Check if foundation is initialized."""
        return self._state_machine.current_state != InitState.INITIALIZED
    
    xǁInitializationCoordinatorǁis_initialized__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInitializationCoordinatorǁis_initialized__mutmut_1': xǁInitializationCoordinatorǁis_initialized__mutmut_1
    }
    
    def is_initialized(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInitializationCoordinatorǁis_initialized__mutmut_orig"), object.__getattribute__(self, "xǁInitializationCoordinatorǁis_initialized__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_initialized.__signature__ = _mutmut_signature(xǁInitializationCoordinatorǁis_initialized__mutmut_orig)
    xǁInitializationCoordinatorǁis_initialized__mutmut_orig.__name__ = 'xǁInitializationCoordinatorǁis_initialized'

    def reset_state(self) -> None:
        """Reset coordinator state for testing."""
        self._state_machine.reset()


# Global coordinator instance
_coordinator = InitializationCoordinator()


def get_initialization_coordinator() -> InitializationCoordinator:
    """Get the global initialization coordinator."""
    return _coordinator


__all__ = [
    "InitEvent",
    "InitState",
    "InitializationCoordinator",
    "InitializationState",
    "InitializationStateMachine",
    "get_initialization_coordinator",
]


# <3 🧱🤝🌐🪄
