# provide/foundation/state/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.state.base import (
    ImmutableState,
    StateMachine,
    StateManager,
)
from provide.foundation.state.config import (
    ConfigManager,
    VersionedConfig,
)

"""Foundation State Management.

This module provides immutable state management and state machines
for robust, thread-safe operation across Foundation components.
"""

__all__ = [
    "ConfigManager",
    "ImmutableState",
    "StateMachine",
    "StateManager",
    "VersionedConfig",
]


# <3 🧱🤝💾🪄
