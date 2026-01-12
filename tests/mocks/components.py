#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Mock components for testing."""

from typing import Any


class MockEntryPoint:
    """Mock entry point for testing component discovery."""

    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self._value = value
        self.module = "test.module"
        self.attr = name

    def load(self) -> Any:
        return self._value


class MockEntryPointGroup:
    """Mock entry points group for testing."""

    def __init__(self, entries: dict[str, list[MockEntryPoint]] | None = None) -> None:
        self.entries = entries or {}

    def select(self, group: str) -> list[MockEntryPoint]:
        return self.entries.get(group, [])


# 🧱🏗️🔚
