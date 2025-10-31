#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.concurrency.async_locks import (
    AsyncLockInfo,
    AsyncLockManager,
    get_async_lock_manager,
    register_foundation_async_locks,
)
from provide.foundation.concurrency.core import (
    async_gather,
    async_run,
    async_sleep,
    async_wait_for,
)
from provide.foundation.concurrency.locks import (
    LockInfo,
    LockManager,
    get_lock_manager,
    register_foundation_locks,
)

"""Concurrency utilities for Foundation.

Provides consistent async/await patterns, task management,
and concurrency utilities for Foundation applications.
"""

__all__ = [
    "AsyncLockInfo",
    "AsyncLockManager",
    "LockInfo",
    "LockManager",
    "async_gather",
    "async_run",
    "async_sleep",
    "async_wait_for",
    "get_async_lock_manager",
    "get_lock_manager",
    "register_foundation_async_locks",
    "register_foundation_locks",
]

# 🧱🏗️🔚
