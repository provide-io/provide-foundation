#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from attrs import define
from provide.testkit import FoundationTestCase

from provide.foundation.state import (
    ImmutableState,
    StateManager,
)


class TestImmutableState(FoundationTestCase):
    def test_initial_state(self) -> None:
        state = ImmutableState()
        assert state.generation == 0
        assert isinstance(state.created_at, float)

    def test_with_changes(self) -> None:
        state1 = ImmutableState()
        state2 = state1.with_changes(generation=5)  # Deliberately setting generation
        assert state2.generation == 5
        assert state1.generation == 0  # Original is unchanged

    def test_with_changes_increments_generation(self) -> None:
        @define(frozen=True, slots=True)
        class CustomState(ImmutableState):
            value: int = 0

        state1 = CustomState()
        state2 = state1.with_changes(value=10)
        assert state2.generation == 1
        assert state2.value == 10
        assert state1.generation == 0
        assert state1.value == 0


class TestStateManager(FoundationTestCase):
    def test_initial_state(self) -> None:
        initial = ImmutableState()
        manager = StateManager(state=initial)
        assert manager.current_state is initial
        assert manager.generation == 0

    def test_update_state(self) -> None:
        manager = StateManager(state=ImmutableState())
        old_state = manager.current_state
        new_state = manager.update_state(generation=10)
        assert manager.current_state is new_state
        assert new_state.generation == 10
        assert old_state.generation == 0


# 🧱🏗️🔚
