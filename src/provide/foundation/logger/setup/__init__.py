#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Foundation Logger Setup Module.

Handles structured logging configuration, processor setup, and emoji resolution.
Provides the core setup functionality for the Foundation logging system."""

from __future__ import annotations

from provide.foundation.logger.setup.coordinator import (
    get_system_logger,
    internal_setup,
)

__all__ = [
    "get_system_logger",
    "internal_setup",
]

# 🧱🏗️🔚
