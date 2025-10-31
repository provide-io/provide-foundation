#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any, Protocol

"""Type definitions for the hub module."""


class Registrable(Protocol):
    """Protocol for objects that can be registered."""

    __registry_name__: str
    __registry_dimension__: str
    __registry_metadata__: dict[str, Any]


# 🧱🏗️🔚
